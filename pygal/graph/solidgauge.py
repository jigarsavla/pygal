


from math import pi, sqrt, sin, cos

from pygal.graph.graph import Graph
from pygal.util import alter, decorate

class SolidGauge(Graph):

    """
    Solid Guage
    For each series a solid guage is shown on the plot area.

    See http://en.wikipedia.org/wiki/#####
    """

    def gaugify(self, serie, startangle, squares, sq_dimensions, current_square):
        serie_node = self.svg.serie(serie)
        metadata = serie.metadata.get(0)
        if 'maxvalue' in metadata.keys():
            maxvalue = metadata['maxvalue']
        else:
            maxvalue = serie.values[0] * 1.5
        if self.half_pie:
            center = ((current_square[1]*sq_dimensions[0]) - (sq_dimensions[0] / 2.),
                      (current_square[0]*sq_dimensions[1]) - (sq_dimensions[1] / 4))
        else:
            center = ((current_square[1]*sq_dimensions[0]) - (sq_dimensions[0] / 2.),
                      (current_square[0]*sq_dimensions[1]) - (sq_dimensions[1] / 2.))

        radius = min([sq_dimensions[0]/2, sq_dimensions[1]/2])
        value = serie.values[0]
        ratio = value / maxvalue
        if self.half_pie:
            angle = 2 * pi * ratio / 2
            endangle = pi / 2
        else:
            angle = 2 * pi * ratio
            endangle = 2 * pi
        value = self._format(serie)

        gauge_ = decorate(
            self.svg,
            self.svg.node(serie_node['plot'], class_="gauge"),
            metadata)


        big_radius = radius * .9
        small_radius = radius * serie.inner_radius
        maxvalue = Maxvalue(serie)
        print(maxvalue.values)
        alter(self.svg.solidgauge(
                serie_node, gauge_, big_radius, small_radius,
                angle, startangle, center, value, 0, metadata, self.half_pie, endangle, self._format(maxvalue)), metadata)

    def _compute_x_labels(self):
        pass

    def _compute_y_labels(self):
        pass

    def _plot(self):
        """Draw all the serie slices"""
        squares = self._squares()
        sq_dimensions = self.add_squares(squares)
        if self.half_pie:
            startangle = 3*pi/2
        else:
            startangle = 0

        for index, serie in enumerate(self.series):
            current_square = self._current_square(squares, index)
            self.gaugify(serie, startangle, squares, sq_dimensions, current_square)

    def _squares(self):

        n_series_ = len(self.series)
        i = 2

        if sqrt(n_series_).is_integer():
            _x = int(sqrt(n_series_))
            _y = int(sqrt(n_series_))
        else:
            while i * i < n_series_:
                while n_series_ % i == 0:
                    n_series_ = n_series_ / i
                i = i + 1
            _y = int(n_series_)
            _x = int(n_series_ / len(self.series))
            if len(self.series) == 5:
                _x, _y = 2, 3
            if abs(_x - _y) > 2:
                _sq = 3
                while (_x * _y)-1 < len(self.series):
                    _x, _y = _sq, _sq
                    _sq += 1
        return (_x, _y)

    def _current_square(self, squares, index):
        current_square = [1, 1]
        steps = index + 1
        steps_taken = 0
        for i in range(squares[0] * squares[1]):
            steps_taken += 1
            if steps_taken != steps and steps_taken % squares[0] != 0:
                current_square[1] += 1
            elif steps_taken != steps and steps_taken % squares[0] == 0:
                current_square[1] = 1
                current_square[0] += 1
            else:
                return tuple(current_square)
        return print('Something went wrong with the current square assignment.')

class Maxvalue(SolidGauge):

    def __init__(self, serie):
        self.serie = serie

    @property
    def values(self):
        try:
            return [self.serie.metadata[0]['maxvalue']]
        except:
            return [self.serie.values[0] * 1.5]

    @property
    def title(self):
        return self.serie.title
