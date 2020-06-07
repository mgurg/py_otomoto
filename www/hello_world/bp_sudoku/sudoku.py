from flask import Blueprint, render_template, flash
from flask import current_app as app

# Blueprint Configuration
sudoku_bp = Blueprint('sudoku_bp', __name__,
                    template_folder='templates')

@sudoku_bp.route('/sudoku')
def sudoku():
    return render_template('sudoku.html')