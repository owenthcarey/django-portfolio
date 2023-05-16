import base64
from io import BytesIO
from PIL import Image
import numpy as np

from django.http import HttpRequest, HttpResponse
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
