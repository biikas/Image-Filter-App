import os
from flask import Flask, render_template, request, redirect, url_for, session
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for the session

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling image upload
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the uploaded file from the form
        image_file = request.files['image']

        # Check if the file is an image
        if image_file and allowed_file(image_file.filename):
            # Save the uploaded image to a temporary location
            image_path = os.path.join('static', 'uploads', 'original.png')
            image_file.save(image_path)

            # Store the original image path and applied filters list in the session
            session['original_image_path'] = image_path
            session['image_path'] = image_path
            session['applied_filters'] = []

    # Redirect back to the main page after the upload
    return redirect(url_for('index'))

# Helper function to check if the file has an allowed extension (e.g., PNG, JPG)
def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Route for applying filters to the image
@app.route('/apply_filters', methods=['POST'])
def apply_filters():
    if 'image_path' in session and request.method == 'POST':
        # Get the stored image path from the session
        image_path = session['image_path']

        # Get the selected filter from the form
        selected_filter = request.form.get('filter')

        # Apply the selected filter to the image
        filtered_image_path = apply_filter(image_path, selected_filter)

        # Update the session with the filtered image path and applied filters list
        session['image_path'] = filtered_image_path
        applied_filters = session.get('applied_filters', [])
        applied_filters.append(selected_filter)
        session['applied_filters'] = applied_filters

    # Redirect back to the main page after applying the filter
    return redirect(url_for('index'))

# Helper function to apply the selected filter to the image and save the output
def apply_filter(image_path, selected_filter):
    original_image = Image.open(image_path)

    if selected_filter == 'blur':
        filtered_image = original_image.filter(ImageFilter.BLUR)
    elif selected_filter == 'sharpen':
        filtered_image = original_image.filter(ImageFilter.SHARPEN)
    elif selected_filter == 'brightness':
        enhanced = ImageEnhance.Brightness(original_image)
        filtered_image = enhanced.enhance(1.5)  # Increase brightness (1.0 is the default)
    elif selected_filter == 'saturation':
        enhanced = ImageEnhance.Color(original_image)
        filtered_image = enhanced.enhance(1.5)  # Increase saturation (1.0 is the default)
    elif selected_filter == 'black_and_white':
        filtered_image = original_image.convert("L")  # Convert to grayscale (black & white)
    elif selected_filter == 'invert':
        filtered_image = ImageOps.invert(original_image)
    else:
        # If no filter is selected, return the original image
        return image_path

    # Save the filtered image to a new location
    filtered_image_path = os.path.join('static', 'uploads', 'filtered.png')
    filtered_image.save(filtered_image_path)

    return filtered_image_path

# Route for the "Get Original" button action
@app.route('/get_original', methods=['POST'])
def get_original():
    if 'original_image_path' in session:
        # Get the stored original image path from the session
        original_image_path = session['original_image_path']

        # Display the original image
        session['image_path'] = original_image_path

    # Redirect back to the main page after getting the original image
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
