

class Metalabeling_settings:
    # =============================== METALABELING SETTINGS =======================
    def gen_metalabels_settings(self):
        # -- Metalabeling settings:
        self.metalabeling_settings = ["Peak", "Simple", "Hybrid"]
        self.metalabeling_setting = 0

        self.upper_barrier = 20
        self.lower_barrier = -20
        self.look_ahead = 20
