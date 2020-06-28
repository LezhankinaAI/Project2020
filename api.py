from flask import Flask
from flask_restful import Api, Resource, reqparse
from WardHierarchicalClustering import cluster_Ward

experiments = {}


class ExperimentDetail(Resource):
    def get(self, id_exp = 0):
        if id_exp in experiments:
            return experiments[id_exp], 200
        return f"Experiment {id_exp} not found", 404

    def post(self, id_exp):
        parser = reqparse.RequestParser()
        parser.add_argument("algo")
        parser.add_argument("data")
        params = parser.parse_args()
        if id_exp in experiments:
            return f"Experiment with id {id_exp} already exists", 400
        if params["algo"] != "cluster_Ward":
            return "Algorithm should be cluster_Ward", 400
        if params["data"] is None:
            return "Empty database", 404
        dataset = params["data"]
        groups = cluster_Ward(dataset, len(dataset[0]), 1)
        experiments[id_exp] = groups
        return groups, 201

    def delete(self, id_exp):
        global experiments
        if id_exp in experiments:
            del experiments[id_exp]
            return f"Experiment with id {id_exp} is deleted.", 200
        return f"Experiment {id_exp} not found", 404


class ExperimentList(Resource):
    def get(self):
        return experiments

    def post(self):
        id_exp = 0
        if len(experiments) == 0:
            experiments[id_exp] = {}
            return experiments[id_exp], 201
        for elem in experiments.keys():
            if elem > id_exp:
                id_exp = elem
        experiments[id_exp + 1] = {}
        return experiments[id_exp + 1], 201


# Create the API object
app = Flask(__name__)
api = Api(app)
api.add_resource(ExperimentList, '/experiments',
                 '/', '/experiments/',
                 endpoint='experiments')
api.add_resource(ExperimentDetail, '/experiments/<int:exp_id>')

# Start the flask loop
if __name__ == '__main__':
    app.run()
