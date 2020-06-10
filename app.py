import concur as c

from src.features.nice_feature.nice_feature_gui import nice_feature_gui, NiceFeatureState


class State:
	def __init__(self):
		# Two identical features for fun.
		self.feature1 = NiceFeatureState(True)
		self.feature2 = NiceFeatureState(False)


def create_main_view(state):
	return c.orr([
		c.main_menu_bar(widget=c.orr([
			c.menu(label="File", widget=c.orr([
				c.menu_item("Do things"),
				c.menu_item("Do other things"),
			])),
		])),

		c.button("Hide Feature 1") if state.feature1.window_visible else c.button("Show Feature 1"),
		c.button("Hide Feature 2") if state.feature2.window_visible else c.button("Show Feature 2"),
		c.button("Quit"),
		c.key_press("Quit", ord('Q'), ctrl=True),

		c.tag("Modify Feature 1", c.optional(state.feature1.window_visible, nice_feature_gui, state.feature1, "Feature 1")),
		c.tag("Modify Feature 2", c.optional(state.feature2.window_visible, nice_feature_gui, state.feature2, "Feature 2")),
	])


def app():
	state = State()
	while True:
		tag, value = yield from create_main_view(state)

		if tag == "Show Feature 1":
			state.feature1.window_visible = True
		elif tag == "Hide Feature 1":
			state.feature1.window_visible = False

		elif tag == "Show Feature 2":
			state.feature2.window_visible = True
		elif tag == "Hide Feature 2":
			state.feature2.window_visible = False

		# This is not strictly necessary, but may be useful for the Undo operation or something.
		elif tag == "Modify Feature 1":
			state.feature1 = value
		elif tag == "Modify Feature 2":
			state.feature2 = value

		elif tag == "Quit":
			break

		else:
			print(f"Unhandled event: {tag}")
		yield


if __name__ == "__main__":
	c.main(widget=app(), name="Nice Application", menu_bar=True)
