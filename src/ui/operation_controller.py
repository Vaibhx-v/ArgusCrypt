class OperationController:

    def __init__(self, progress_panel, activity_panel, status_panel):

        self.progress = progress_panel
        self.activity = activity_panel
        self.status = status_panel

    # ---------------- ENCRYPTION ---------------- #

    def start_encryption(self, filename):

        self.activity.clear()

        self.status.update_file(filename)

        self.status.encrypting()

        self.progress.reset()

    def validate_password(self):

        self.progress.update_progress(
            15,
            "Validating Password..."
        )

        self.activity.log(
            "Password Validated"
        )

    def generate_salt(self):

        self.progress.update_progress(
            30,
            "Generating Salt..."
        )

        self.activity.log(
            "Salt Generated"
        )

    def derive_key(self):

        self.progress.update_progress(
            50,
            "Deriving AES Key..."
        )

        self.activity.log(
            "AES Key Derived"
        )

    def encrypting(self):

        self.progress.update_progress(
            75,
            "Encrypting Image..."
        )

        self.activity.log(
            "Encrypting..."
        )

    def saving(self):

        self.progress.update_progress(
            95,
            "Saving File..."
        )

        self.activity.log(
            "Saved Successfully"
        )

    def success(self):

        self.progress.update_progress(
            100,
            "Completed"
        )

        self.activity.log(
            "Encryption Successful"
        )

        self.status.success()

    # ---------------- DECRYPTION ---------------- #

    def start_decryption(self, filename):

        self.activity.clear()

        self.status.update_file(filename)

        self.status.decrypting()

        self.progress.reset()

    def decrypting(self):

        self.progress.update_progress(
            60,
            "Decrypting..."
        )

        self.activity.log(
            "Decrypting File"
        )

    def restoring(self):

        self.progress.update_progress(
            90,
            "Restoring Image..."
        )

        self.activity.log(
            "Restoring Original Image"
        )

    def decryption_success(self):

        self.progress.update_progress(
            100,
            "Completed"
        )

        self.activity.log(
            "Decryption Successful"
        )

        self.status.success()

    # ---------------- FAILURE ---------------- #

    def failed(self, message):

        self.activity.error(message)

        self.status.failed()