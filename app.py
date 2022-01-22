from flask import Flask
from flask_restful import Resource, Api, reqparse
from fraction_calc_binary_tree import BinaryFractionBTree
from fraction_calculator_math import get_fractional

app = Flask(__name__)
api = Api(app)


class BinaryTreeUsage(Resource):
    precision_level = 5
    decimal_fraction = None
    result_fraction = None
    whole = None
    numerator = None
    denominator = None

    def get(self):
        return self._get_result()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('decimal_fraction', type=float, required=True)
        parser.add_argument(
            'precision_level',
            type=int,
            default=5,
            choices=[2, 3, 4, 5, 6],
            help='Which value for power of two should be used for precision. Valid values are in range 2-6 inclusive')
        args = parser.parse_args(strict=True)
        self.precision_level = args["precision_level"]
        self.decimal_fraction = args["decimal_fraction"]
        self._find_nearest_fraction()
        return self._get_result()

    def _find_nearest_fraction(self):
        if self.decimal_fraction.is_integer():
            self.result_fraction = str(int(self.decimal_fraction))
            self.whole = int(self.decimal_fraction)
        else:
            self.whole = int(self.decimal_fraction)
            frac_str = str(self.decimal_fraction).split('.')[1]
            decimal_factor = 10 ** len(frac_str)
            fraction = int(frac_str)
            ff = BinaryFractionBTree(self.precision_level)
            self.numerator, self.denominator = ff.find_nearest(fraction / decimal_factor)
            self.result_fraction = f"{self.whole} {self.numerator} / {self.denominator}"

    def _get_result(self):
        return {
            "decimal": self.decimal_fraction,
            "precision": self.precision_level,
            "fraction": self.result_fraction,
            "whole": self.whole,
            "numerator": self.numerator,
            "denominator": self.denominator
        }


class SingleMethodUsage(Resource):
    precision = 64
    decimal_fraction = None
    result_fraction = None
    whole = None
    numerator = None
    denominator = None

    def get(self):
        return self._get_result()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('decimal_fraction', type=float, required=True)
        parser.add_argument(
            'denominator',
            type=int,
            default=64,
            choices=[2, 4, 8, 16, 32, 64, 128],
            help='Fraction of this value should be used. Default is 64'
        )
        args = parser.parse_args(strict=True)
        self.precision = args['denominator']
        self.decimal_fraction = args['decimal_fraction']
        self.whole, self.numerator, self.denominator = get_fractional( self.decimal_fraction, self.precision)
        self.result_fraction = f"{self.whole} {self.numerator} / {self.denominator}"
        return self._get_result()

    def _get_result(self):
        return {
            "decimal": self.decimal_fraction,
            "precision": self.precision,
            "fraction": self.result_fraction,
            "whole": self.whole,
            "numerator": self.numerator,
            "denominator": self.denominator
        }


api.add_resource(BinaryTreeUsage, '/btree')
api.add_resource(SingleMethodUsage, '/math')

if __name__ == '__main__':
    app.run()
