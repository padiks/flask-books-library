from flask import Blueprint, render_template, request

# Define a Blueprint for the module
primer_bp = Blueprint(
    "primer",  # Blueprint name
    __name__,  # Current module (helps with finding templates)
    template_folder="templates"  # Folder where templates are stored
)

# ---------------------------
# Route for the Blueprint View
# ---------------------------
@primer_bp.route("/", methods=["GET", "POST"])  # Allow both GET and POST requests
def view():
    """
    This function handles the request to the root of the blueprint.
    It renders the corresponding template and passes variables to it.
    """
    
    # 1. Store a message to display in the template
    hello_message = "Hello, World!"
    
    # 2. Default values for the numbers (for sum calculation)
    first_number = 48
    second_number = 50
    sum_result = first_number + second_number  # This is static and should not change
    
    # 3. Handle the POST request to retrieve user inputs and calculate the result using a formula
    result = None  # To hold the result of multiplication (None if not calculated)
    
    if request.method == "POST":
        # Get user input from the form for multiplication
        first_number_input = float(request.form.get("num1", first_number))  # Default to previous value if no input
        second_number_input = float(request.form.get("num2", second_number))  # Default to previous value if no input

        # Calculate the multiplication
        result = first_number_input * second_number_input  # Perform multiplication only
    
    # Render the template and pass variables to it
    return render_template(
        "primer/view.html", 
        message=hello_message, 
        sum=sum_result,  # Pass the static sum that doesn’t change
        result=result  # Pass the dynamic multiplication result
    )
