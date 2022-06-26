import logging


class EpaperState:
    states = {}

    def dirty(self):
        d = False
        for state_key in self.states:
            if self.states[state_key].dirty:
                logging.debug("dirty state")
                d = True
                break
        return d

    def refresh(self, force=False):
        for state_key in self.states:
            self.states[state_key].refresh(force=force)

    def make_dirty(self):
        for state_key in self.states:
            self.states[state_key].dirty = True
            break  # only one dirty flag is enough
