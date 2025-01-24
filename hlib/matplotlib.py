class AxesEventDetector:
    """
    event_name : str
        events to connect the return function to. examples:
            'button_press_event'  : returns point that is pressed
            'motion_notify_event' : returns event every time mouse is moved
    """
    def __init__(self, ax, event_name, return_function, active = True):
        self.ax = ax
        self.event_name = event_name
        self.return_function = return_function
        self.active = active

        self.cid = None
        if self.active:
            self._activate()

    def _activate(self):
        self.cid = self.ax.figure.canvas.mpl_connect(self.event_name, self.on_event)

    def _deactivate(self):
        self.ax.figure.canvas.mpl_disconnect(self.cid)
        self.cid = None

    def set_active(self, active : bool):
        if active and not self.active:
            self._activate()
        elif (not active) and self.active:
            self._deactivate()
        self.active = active

    def on_event(self, event):
        if event.inaxes is self.ax:
            self.return_function(event)

class HiddenScatterAnnotation:
    """
    scatter is the collection returned by a call to plt.scatter()
    get_text_function is a function that takes the index of a point and 
    returns the text that should be put in its annotation

    annotation can be modified by calls to the annotation property
    """
    def __init__(self, scatter, get_text_function, active = True):
        self.scatter = scatter
        self.get_text_function = get_text_function
        self.active = active

        self.annotation = self.scatter.axes.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->")
        )
        self.annotation.set_visible(False)

        self.event_detector = AxesEventDetector(
                self.scatter.axes, "motion_notify_event", self.hover, self.active
        )

    def set_active(self, active : bool):
        self.event_detector.set_active(active)
        self.active = active

    def update_annotation(self, index):
        position = self.scatter.get_offsets()[index]
        self.annotation.xy = position

        text = self.get_text_function(index)
        self.annotation.set_text(text)
        self.annotation.get_bbox_patch().set_alpha(1.0)

    def hover(self, event):
        visible = self.annotation.get_visible()
        contains, index_dict = self.scatter.contains(event)
        if contains:
            self.update_annotation(index_dict["ind"][-1])
            self.annotation.set_visible(True)
            self.scatter.axes.figure.canvas.draw_idle()
        else:
            if visible:
                self.annotation.set_visible(False)
                self.scatter.axes.figure.canvas.draw_idle()
