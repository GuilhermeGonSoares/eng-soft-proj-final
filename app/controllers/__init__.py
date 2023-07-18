def blueprints():
    from .auth_controller import bp as auth_blueprint
    from .student_controller import bp as student_blueprint
    from .teacher_controller import bp as teacher_blueprint

    return [auth_blueprint, student_blueprint, teacher_blueprint]