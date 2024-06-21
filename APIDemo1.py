import json
from flask import Flask, jsonify, request

app = Flask(__name__)

employees = [{'id': 1, 'name': 'Ashley'}, {'id': 2, 'name': 'Kate'}, {'id': 3, 'name': 'Joe'}]


@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)


@app.route('/employees/<int:id>', methods=['GET'])
def get_employee_by_id(id: int):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404
    return jsonify(employee)


def get_employee(id):
    return next((e for e in employees if e['id'] == id), None)


def employee_is_valid(employee):
    for key in employee.keys():
        if key != 'name':
            return False
    return True


if __name__ == '__main__':
    app.run(port=5000)
