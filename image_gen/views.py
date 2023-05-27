import base64
from io import BytesIO
from PIL import Image, ImageDraw
import numpy as np
import os
import zipfile

from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render
import keras_cv
import math


def generate_image(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        prompt = request.POST.get("prompt", None)
        if prompt:
            model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)
            images = model.text_to_image(prompt, batch_size=1, num_steps=50)
            buffer = BytesIO()
            img_pil = Image.fromarray(np.uint8(images[0] * 255))
            img_pil.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode()
            return render(request, "image_gen/display_image.html", {"image": img_str})
    return render(request, "image_gen/input_prompt.html")


def draw_star(draw, start, size, points=10, fill="white"):
    degrees_per_point = 360 / points
    rad_per_deg = math.pi / 180
    radius_outer = size // 2
    radius_inner = radius_outer // 2

    points_outer = [(start + size // 2 + radius_outer * math.cos(rad_per_deg * (i * degrees_per_point)),
                     start + size // 2 + radius_outer * math.sin(rad_per_deg * (i * degrees_per_point)))
                    for i in range(points)]

    points_inner = [(start + size // 2 + radius_inner * math.cos(rad_per_deg * ((i + 0.5) * degrees_per_point)),
                     start + size // 2 + radius_inner * math.sin(rad_per_deg * ((i + 0.5) * degrees_per_point)))
                    for i in range(points)]

    star_points = [val for pair in zip(points_outer, points_inner) for val in pair]
    draw.polygon(star_points, fill=fill)


def generate_app_icon(request: HttpRequest) -> FileResponse:
    # Get the user's input.
    color = request.GET.get("color", "#000000")
    prompt = request.GET.get("prompt", "Default Prompt")

    # Prepare to save the files in a temporary directory.
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Generate the app icon.
    base_size = 1024
    ios_square_size = base_size * 0.8  # 80% of the base_size
    android_square_size = base_size * 0.70  # 70% of the base_size

    ios_square_start = (base_size - ios_square_size) // 2
    android_square_start = (base_size - android_square_size) // 2

    # # Generate the iOS app icon.
    # ios_img = Image.new("RGB", (base_size, base_size), color=color)
    # draw_ios = ImageDraw.Draw(ios_img)
    # draw_ios.rectangle(
    #     [
    #         ios_square_start,
    #         ios_square_start,
    #         ios_square_start + ios_square_size,
    #         ios_square_start + ios_square_size,
    #     ],
    #     fill="white",
    # )
    #
    # # Generate the Android app icon.
    # android_img = Image.new("RGB", (base_size, base_size), color=color)
    # draw_android = ImageDraw.Draw(android_img)
    # draw_android.rectangle(
    #     [
    #         android_square_start,
    #         android_square_start,
    #         android_square_start + android_square_size,
    #         android_square_start + android_square_size,
    #     ],
    #     fill="white",
    # )

    # Generate the iOS app icon.
    ios_img = Image.new("RGB", (base_size, base_size), color=color)
    draw_ios = ImageDraw.Draw(ios_img)
    draw_star(draw_ios, ios_square_start, ios_square_size)

    # Generate the Android app icon.
    android_img = Image.new("RGB", (base_size, base_size), color=color)
    draw_android = ImageDraw.Draw(android_img)
    draw_star(draw_android, android_square_start, android_square_size)

    # Resize the app icons and save all the sizes.
    ios_sizes = [20, 29, 40, 58, 60, 76, 80, 87, 120, 152, 167, 180, 1024]
    android_sizes = [48, 72, 96, 144, 192, 512]

    for size in ios_sizes:
        resized_img = ios_img.resize((size, size))
        resized_img.save(f"{temp_dir}/iOS_{prompt}_{size}.png")

    for size in android_sizes:
        resized_img = android_img.resize((size, size))
        resized_img.save(f"{temp_dir}/Android_{prompt}_{size}.png")

    # Compile the app icons into a ZIP file.
    zip_filename = f"{prompt}_app_icons.zip"
    zipf = zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

    # Provide the ZIP file for download.
    response = FileResponse(open(zip_filename, "rb"))
    response["Content-Type"] = "application/zip"
    response["Content-Disposition"] = f"attachment; filename={zip_filename}"

    # Delete the temp files and directory.
    for file in os.listdir(temp_dir):
        os.remove(f"{temp_dir}/{file}")
    os.rmdir(temp_dir)
    os.remove(zip_filename)

    return response
