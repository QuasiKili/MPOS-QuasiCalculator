from mpos.apps import Activity
import mpos.ui

class Kilculator(Activity):

    display = None
    current_value = "0"
    operator = None
    previous_value = None
    scientific_mode = False
    screen = None
    btnm = None

    def onCreate(self):
        self.screen = lv.obj()
        self.screen.set_style_pad_all(0, 0)

        # Display container with border
        display_cont = lv.obj(self.screen)
        display_cont.set_size(lv.pct(100), 50)
        display_cont.align(lv.ALIGN.TOP_MID, 0, 0)
        display_cont.set_style_border_width(2, lv.PART.MAIN)
        display_cont.set_style_border_color(lv.theme_get_color_primary(None), lv.PART.MAIN)
        display_cont.set_style_radius(0, 0)
        display_cont.set_style_pad_all(5, 0)

        # Display label
        self.display = lv.label(display_cont)
        self.display.set_text("0")
        self.display.align(lv.ALIGN.RIGHT_MID, -5, 0)
        self.display.set_style_text_font(lv.font_montserrat_20, 0)

        # Create initial button layout
        self.create_button_matrix()

        self.setContentView(self.screen)

    def toggle_mode(self):
        self.scientific_mode = not self.scientific_mode
        if self.btnm:
            self.btnm.delete()
        self.create_button_matrix()

    def create_button_matrix(self):
        if self.scientific_mode:
            btnm_map = [
                "7", "8", "9", "/", "sqrt", "\n",
                "4", "5", "6", "*", "^", "\n",
                "1", "2", "3", "-", "%", "\n",
                "STD", "0", ".", "+", "=", "\n",
                "C", "sin", "cos", "tan", "log", ""
            ]
        else:
            btnm_map = [
                "7", "8", "9", "/", "\n",
                "4", "5", "6", "*", "\n",
                "1", "2", "3", "-", "\n",
                "SCI", "0", ".", "+", "\n",
                "C", "=", ""
            ]

        self.btnm = lv.buttonmatrix(self.screen)
        self.btnm.set_map(btnm_map)

        # Responsive sizing - fill remaining space below display
        self.btnm.set_size(lv.pct(100), mpos.ui.pct_of_display_height(79))
        self.btnm.align(lv.ALIGN.BOTTOM_MID, 0, 0)
        self.btnm.add_event_cb(self.button_event, lv.EVENT.VALUE_CHANGED, None)

        # Style focused button to be more visible
        self.btnm.set_style_border_width(2, lv.PART.ITEMS | lv.STATE.FOCUSED)
        self.btnm.set_style_border_color(lv.theme_get_color_primary(None), lv.PART.ITEMS | lv.STATE.FOCUSED)

        # Make button matrix focusable
        focusgroup = lv.group_get_default()
        if focusgroup:
            focusgroup.add_obj(self.btnm)

    def button_event(self, event):
        import math
        btnm = event.get_target_obj()
        idx = btnm.get_selected_button()
        text = btnm.get_button_text(idx)

        if text in ["SCI", "STD"]:
            self.toggle_mode()
            return

        if text.isdigit():
            if self.current_value == "0":
                self.current_value = text
            else:
                self.current_value += text
            self.display.set_text(self.current_value)

        elif text == ".":
            if "." not in self.current_value:
                self.current_value += "."
                self.display.set_text(self.current_value)

        elif text == "pi":
            self.current_value = str(math.pi)
            self.display.set_text(self.current_value)

        elif text == "sqrt":
            current = float(self.current_value)
            result = math.sqrt(current) if current >= 0 else 0
            self.current_value = str(int(result) if result == int(result) else result)
            self.display.set_text(self.current_value)

        elif text == "sin":
            if self.scientific_mode:
                current = float(self.current_value)
                result = math.sin(math.radians(current))
                self.current_value = str(int(result) if result == int(result) else result)
                self.display.set_text(self.current_value)

        elif text == "cos":
            if self.scientific_mode:
                current = float(self.current_value)
                result = math.cos(math.radians(current))
                self.current_value = str(int(result) if result == int(result) else result)
                self.display.set_text(self.current_value)

        elif text == "tan":
            if self.scientific_mode:
                current = float(self.current_value)
                result = math.tan(math.radians(current))
                self.current_value = str(int(result) if result == int(result) else result)
                self.display.set_text(self.current_value)

        elif text == "log":
            if self.scientific_mode:
                current = float(self.current_value)
                result = math.log10(current) if current > 0 else 0
                self.current_value = str(int(result) if result == int(result) else result)
                self.display.set_text(self.current_value)

        elif text in ["+", "-", "*", "/", "^", "%"]:
            if self.previous_value is None:
                self.previous_value = float(self.current_value)
                self.current_value = "0"
            self.operator = text

        elif text == "=":
            if self.operator and self.previous_value is not None:
                current = float(self.current_value)
                if self.operator == "+":
                    result = self.previous_value + current
                elif self.operator == "-":
                    result = self.previous_value - current
                elif self.operator == "*":
                    result = self.previous_value * current
                elif self.operator == "/":
                    result = self.previous_value / current if current != 0 else 0
                elif self.operator == "^":
                    result = self.previous_value ** current
                elif self.operator == "%":
                    result = self.previous_value % current if current != 0 else 0

                self.current_value = str(int(result) if result == int(result) else result)
                self.display.set_text(self.current_value)
                self.previous_value = None
                self.operator = None

        elif text == "C":
            self.current_value = "0"
            self.previous_value = None
            self.operator = None
            self.display.set_text("0")

