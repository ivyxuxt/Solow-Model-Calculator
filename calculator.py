import math
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
from flask import Flask, render_template_string, request

# Flask app setup
app = Flask(__name__)


# Solow model functions
def steady_state_k(avg_s, avg_pop_gr, pro_gr, depreciation_rate, k_share):
    return (avg_s / (avg_pop_gr + pro_gr + depreciation_rate)) ** (1 / (1 - k_share))


def steady_state_y(avg_s, avg_pop_gr, pro_gr, depreciation_rate, k_share):
    return (avg_s / (avg_pop_gr + pro_gr + depreciation_rate)) ** (k_share / (1 - k_share))


# HTML template for user input and result display
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solow Model Calculator</title>
</head>
<body>
    <h1>Solow Model Calculator</h1>
    <form method="POST">
        <label for="avg_s">Average Savings Rate (0-1):</label><br>
        <input type="number" id="avg_s" name="avg_s" step="0.01" required><br>

        <label for="avg_pop_gr">Average Population Growth Rate (0-1):</label><br>
        <input type="number" id="avg_pop_gr" name="avg_pop_gr" step="0.01" required><br>

        <label for="pro_gr">Productivity Growth Rate (0-1):</label><br>
        <input type="number" id="pro_gr" name="pro_gr" step="0.01" required><br>

        <label for="depreciation_rate">Depreciation Rate (0-1):</label><br>
        <input type="number" id="depreciation_rate" name="depreciation_rate" step="0.01" required><br>

        <label for="k_share">Capital Share of Income (0-1):</label><br>
        <input type="number" id="k_share" name="k_share" step="0.01" required><br><br>

        <button type="submit">Calculate</button>
    </form>

    {% if result %}
        <h2>Results</h2>
        <p><strong>Steady-State Capital per Effective Labor (k̂):</strong> {{ result["k_hat"] }}</p>
        <p><strong>Steady-State Output per Effective Labor (ŷ):</strong> {{ result["y_hat"] }}</p>
    {% endif %}
</body>
</html>
"""


# Route for the application
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        # Get user inputs
        avg_s = float(request.form["avg_s"])
        avg_pop_gr = float(request.form["avg_pop_gr"])
        pro_gr = float(request.form["pro_gr"])
        depreciation_rate = float(request.form["depreciation_rate"])
        k_share = float(request.form["k_share"])

        # Perform calculations
        k_hat = steady_state_k(avg_s, avg_pop_gr, pro_gr, depreciation_rate, k_share)
        y_hat = steady_state_y(avg_s, avg_pop_gr, pro_gr, depreciation_rate, k_share)

        result = {"k_hat": round(k_hat, 6), "y_hat": round(y_hat, 6)}

    return render_template_string(html_template, result=result)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
