"""
Flask Web Application for Life Trajectory Simulator
Provides API endpoints for simulation and web interface
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from models.person import BirthProfile, Personality
from models.world_base import BaseWorldState
from models.country_china import ChinaCountryModel
from models.city import City, create_china_cities
from engine.simulator_v2 import LifeSimulatorV2
from utils.rng import rng

app = Flask(__name__)
CORS(app)  # Enable CORS for API calls


@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')


@app.route('/api/simulate', methods=['POST'])
def simulate():
    """Run a life simulation based on user input"""
    try:
        data = request.json
        
        # Extract birth profile
        birth = BirthProfile(
            birth_year=int(data.get('birth_year', 1990)),
            region=data.get('region', 'Urban'),
            family_class=float(data.get('family_class', 0.5)),
            parents_education=float(data.get('parents_education', 0.5)),
            family_stability=float(data.get('family_stability', 0.5)),
            genetic_health=float(data.get('genetic_health', 0.7)),
            cognitive_potential=float(data.get('cognitive_potential', 0.6))
        )
        
        # Extract personality
        personality = Personality(
            openness=float(data.get('openness', 0.5)),
            conscientiousness=float(data.get('conscientiousness', 0.5)),
            risk_preference=float(data.get('risk_preference', 0.5)),
            social_drive=float(data.get('social_drive', 0.5)),
            resilience=float(data.get('resilience', 0.5))
        )
        
        # Extract simulation parameters
        country = data.get('country', 'China')
        city_name = data.get('city', 'beijing')
        max_age = int(data.get('max_age', 80))
        seed = data.get('seed')
        
        # Set seed if provided
        if seed is not None:
            rng.set_seed(int(seed))
        
        # Create simulation environment
        base_world = BaseWorldState(year=birth.birth_year, base_year=1949)
        
        if country == 'China':
            country_model = ChinaCountryModel(base_world, birth.birth_year)
            china_cities = create_china_cities()
            if city_name not in china_cities:
                city_name = 'beijing'
            city = City(china_cities[city_name], country_model)
        else:
            # For other countries, use default (can be extended)
            country_model = ChinaCountryModel(base_world, birth.birth_year)
            china_cities = create_china_cities()
            city = City(china_cities['beijing'], country_model)
        
        # Run simulation
        simulator = LifeSimulatorV2(max_age=max_age, seed=seed)
        result = simulator.simulate(birth, personality, country_model, city)
        
        # Format result for frontend
        formatted_result = {
            'success': True,
            'person': result['person'],
            'base_world': result['base_world'],
            'country': result['country'],
            'city': result['city'],
            'events': result['events'],
            'summary': result['summary'],
            'trajectory': _generate_trajectory(result)
        }
        
        return jsonify(formatted_result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


def _generate_trajectory(result):
    """Generate trajectory data for visualization"""
    # This would be populated during simulation
    # For now, return summary data
    person = result['person']
    
    return {
        'final_age': person['age'],
        'final_wealth': person['wealth'],
        'final_income': person['income'],
        'final_education': person['education_level'],
        'final_health': person['health'],
        'final_stress': person['stress'],
        'total_events': len(result['events'])
    }


@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Get available cities for a country"""
    country = request.args.get('country', 'China')
    
    if country == 'China':
        cities = create_china_cities()
        city_list = [
            {
                'id': key,
                'name': config.city_name,
                'tier': config.tier.value,
                'income_ceiling': config.income_ceiling,
                'living_cost': config.living_cost,
                'risk_reward': config.risk_reward_ratio
            }
            for key, config in cities.items()
        ]
        return jsonify({'cities': city_list})
    
    return jsonify({'cities': []})


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

