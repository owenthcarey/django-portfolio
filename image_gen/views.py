import base64
from io import BytesIO
from PIL import Image, ImageDraw
import numpy as np
import os
import zipfile

from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render
import keras_cv


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


def generate_app_icon(request: HttpRequest) -> FileResponse:
    # Step 1: Get the user's input.
    color = request.GET.get("color", "#000000")
    prompt = request.GET.get("prompt", "Default Prompt")

    # Prepare to save the files in a temporary directory.
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Step 2: Generate the app icon.
    base_size = 1024
    square_size = base_size // 2
    square_start = base_size // 4
    img = Image.new("RGB", (base_size, base_size), color=color)
    draw = ImageDraw.Draw(img)
    draw.rectangle(
        [
            square_start,
            square_start,
            square_start + square_size,
            square_start + square_size,
        ],
        fill="white",
    )

    # Step 3: Resize the icon and save all the sizes.
    ios_sizes = [20, 29, 40, 58, 60, 76, 80, 87, 120, 152, 167, 180, 1024]
    for size in ios_sizes:
        resized_img = img.resize((size, size))
        resized_img.save(f"{temp_dir}/{prompt}_{size}.png")

    # Step 4: Compile the icons into a ZIP file.
    zip_filename = f"{prompt}_app_icons.zip"
    zipf = zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

    # Step 5: Provide the ZIP file for download.
    response = FileResponse(open(zip_filename, "rb"))
    response["Content-Type"] = "application/zip"
    response["Content-Disposition"] = f"attachment; filename={zip_filename}"

    # Delete temp files and directory
    for file in os.listdir(temp_dir):
        os.remove(f"{temp_dir}/{file}")
    os.rmdir(temp_dir)
    os.remove(zip_filename)

    return response
