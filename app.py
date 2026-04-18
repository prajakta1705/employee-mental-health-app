from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load ML model
model = joblib.load("model.pkl")

# Store results
results = []

# Store full employee data
employee_data = []

# Home (Employee Form)
@app.route('/')
def home():
    return render_template("form.html")

# Submit form
@app.route('/submit', methods=['POST'])
def submit():
    data = [float(x) for x in request.form.values()]
    
    prediction = model.predict([data])[0]
    
    employee_data.append(data)
    results.append(prediction)
    
    return render_template("thankyou.html")

# HR Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    HR_PASSWORD = "Prajakta@123"

    if request.method == 'POST':
        entered_password = request.form.get('password')

        if entered_password.strip() != HR_PASSWORD:
            return "Access Denied ❌"

        total = len(results)

        if total == 0:
            percent = 0
            need_help = 0
            no_help = 0
        else:
            need_help = sum(results)
            no_help = total - need_help
            percent = (need_help / total) * 100

        # 🔥 INSIGHTS CALCULATION
        work_high = 0
        family_yes = 0
        benefits_no = 0

        for d in employee_data:
            if d[3] >= 2:   # work_interfere
                work_high += 1

            if d[2] == 1:   # family_history
                family_yes += 1

            if d[6] == 0:   # benefits
                benefits_no += 1

        if total > 0:
            work_percent = (work_high / total) * 100
            family_percent = (family_yes / total) * 100
            benefits_percent = (benefits_no / total) * 100
        else:
            work_percent = family_percent = benefits_percent = 0

        return render_template(
            "dashboard.html",
            percent=round(percent,2),
            total=total,
            need_help=need_help,
            no_help=no_help,
            data=employee_data,
            work_percent=round(work_percent,2),
            family_percent=round(family_percent,2),
            benefits_percent=round(benefits_percent,2)
        )

    return render_template("hr_login.html")


if __name__ == "__main__":
    app.run(debug=True)