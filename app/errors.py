"""
Custom error handlers for ExpenseIQ.
"""

from flask import render_template


def register_error_handlers(app):
    """
    Register all application error handlers.
    """

    @app.errorhandler(404)
    def page_not_found(error):
        return (
            render_template(
                "errors/404.html",
                title="Page Not Found",
            ),
            404,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            render_template(
                "errors/500.html",
                title="Internal Server Error",
            ),
            500,
        )
