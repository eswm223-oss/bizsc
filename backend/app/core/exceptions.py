class AppError(Exception):
    """BizSCアプリケーション共通の例外。"""


class UserNotFoundError(AppError):
    """指定されたユーザーが存在しない場合の例外。"""


class EmailAlreadyRegisteredError(AppError):
    """メールアドレスがすでに登録されている場合の例外。"""