from ..view.user_view import UserLoginView, UserDetailView, UserListView, UserSignUpView, AdminSignUpView
from ..utils.error_handler import error_handle


def create_endpoints(app, services, database):
    app.add_url_rule(
        '/sign-up',
        view_func=UserSignUpView.as_view(
            'sign_up_view',
            services,
            database
        )
    )

    app.add_url_rule(
        '/admin/sign-up',
        view_func=AdminSignUpView.as_view(
            'admin_sign_up_view',
            services,
            database
        )
    )

    app.add_url_rule(
        '/login',
        view_func=UserLoginView.as_view(
            'login_view',
            services,
            database
        )
    )

    app.add_url_rule(
        '/users',
        view_func=UserListView.as_view(
            'user_view',
            services,
            database
        )
    )

    app.add_url_rule(
        '/my-page',
        view_func=UserDetailView.as_view(
            'user_detail_view',
            services,
            database
        )
    )

    error_handle(app)
