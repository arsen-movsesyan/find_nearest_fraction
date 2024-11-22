from flask import Flask
from flask_restful import Resource, Api, reqparse
from fraction_calc_binary_tree import BinaryFractionBTree
from fraction_calculator_math import get_fractional
from flask_cors import CORS
from fractions import Fraction


app = Flask(__name__)
CORS(app)
api = Api(app)

btree_precision_choices = [i for i in range(2, 11)]
default_precision = 5


class Algorithms(Resource):

    def get(self):
        return [
            {
                "name": "Binary Tree",
                "description": "Binary Tree used to create the entire tree of available values",
                "github_url": "https://github.com/arsen-movsesyan/find_nearest_fraction/blob/6d9697e4b60c32ee7358b3d7215d65b0c90e74b6/fraction_calc_binary_tree.py",
                "api_endpoint": "btree",
                "precision_choice": btree_precision_choices,
                "default_precision": default_precision
            },
            {
                "name": "Condensed",
                "description": "Single method with condensed algorithm",
                "github_url": "https://github.com/arsen-movsesyan/find_nearest_fraction/blob/6d9697e4b60c32ee7358b3d7215d65b0c90e74b6/fraction_calculator_math.py",
                "api_endpoint": "densed",
                "precision_choice": [2, 4, 8, 16, 32, 64, 128],
                "default_precision": 64
        }
        ]


class ResponseMixin:
    precision = default_precision
    decimal_fraction = None
    result_fraction = None
    whole = None
    numerator = None
    denominator = None

    def get_result(self):
        return {
            "decimal": self.decimal_fraction,
            "precision": self.precision,
            "fraction": self.result_fraction,
            "whole": self.whole,
            "numerator": self.numerator,
            "denominator": self.denominator
        }


class BinaryTreeUsage(Resource, ResponseMixin):

    def get(self):
        return self.get_result()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('decimal_fraction', type=float, required=True)
        parser.add_argument(
            'precision',
            type=int,
            default=self.precision,
            required=False,
            choices=btree_precision_choices,
            help=f'Invalid input. Valid choices are integer values in range from {btree_precision_choices[0]} to {btree_precision_choices[-1]} inclusive')
        args = parser.parse_args(strict=True)
        self.precision = args["precision"]
        self.decimal_fraction = args["decimal_fraction"]
        self._find_nearest_fraction()
        return self.get_result()

    def _find_nearest_fraction(self):
        if self.decimal_fraction.is_integer():
            self.result_fraction = str(int(self.decimal_fraction))
            self.whole = int(self.decimal_fraction)
        else:
            self.whole = int(self.decimal_fraction)
            frac_str = str(self.decimal_fraction).split('.')[1]
            decimal_factor = 10 ** len(frac_str)
            fraction_part = int(frac_str)
            ff = BinaryFractionBTree(self.precision)
            self.numerator, self.denominator = ff.find_nearest(fraction_part / decimal_factor)
            self.result_fraction = f"{self.whole} {self.numerator} / {self.denominator}"


class SingleMethodUsage(Resource, ResponseMixin):
    precision = 64

    def get(self):
        return self.get_result()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('decimal_fraction', type=float, required=True)
        parser.add_argument(
            'precision',
            type=int,
            default=64,
            choices=[2, 4, 8, 16, 32, 64, 128],
            help='Fraction of this value should be used. Default is 64'
        )
        args = parser.parse_args(strict=True)
        self.precision = args['precision']
        self.decimal_fraction = args['decimal_fraction']
        self.whole, self.numerator, self.denominator = get_fractional( self.decimal_fraction, self.precision)
        self.result_fraction = f"{self.whole} {self.numerator} / {self.denominator}"
        return self.get_result()


class FractionToDecimal(Resource, ResponseMixin):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fraction', type=str, required=True)
        parser.add_argument('whole', type=int, required=False)
        parser.add_argument(
            'precision',
            type=int,
            required=False,
            choices=btree_precision_choices,
            default=self.precision,
            help=f"Invalid input. Valid choices are integer values in range from {btree_precision_choices[0]} to {btree_precision_choices[-1]} inclusive"
        )
        args = parser.parse_args(strict=True)
        try:
            fraction = Fraction(args['fraction'])
        except ValueError:
            return {"message": f"Invalid input. Cannot convert to fraction {args['fraction']}"}, 400
        self.numerator = fraction.numerator
        if 'precision' in args:
            self.precision = args['precision']
        self.denominator = fraction.denominator
        self.decimal_fraction = round(self.numerator / self.denominator, self.precision)
        if args['whole'] is not None:
            self.whole = args['whole']
            self.decimal_fraction += abs(self.whole)
            if self.whole < 0:
                self.decimal_fraction *= -1
        self.result_fraction = f"{self.whole} {self.numerator} / {self.denominator}"
        return self.get_result()


api.add_resource(Algorithms, '/algorithms')
api.add_resource(BinaryTreeUsage, '/btree', '/to-binary')
api.add_resource(SingleMethodUsage, '/densed')
api.add_resource(FractionToDecimal, '/to-decimal')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
