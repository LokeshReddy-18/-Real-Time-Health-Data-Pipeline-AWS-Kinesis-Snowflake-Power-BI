import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import boto3
import json


firehose_client = boto3.client(
    'firehose',
    region_name = 'us-east-2',
    aws_access_key_id = '',
    aws_secret_access_key = ''
)


def send_to_firehose(data):
    # Ensure 'data' is a string containing JSON data
    if isinstance(data, str):
        response = firehose_client.put_record(
            DeliveryStreamName='health_data_firehose_stream',
            Record={'Data': data + '\n'}
        )
        print("Firehose response:", response)
    else:
        raise TypeError("Expected 'data' to be a JSON string")



# Constants for simulation
WALKING_SPEED_LOW = 1  # km/h (slow walking)
WALKING_SPEED_MEDIUM = 3  # km/h (regular walking)
WALKING_SPEED_HIGH = 5  # km/h (fast walking)
ACTIVITY_START_TIME = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
ACTIVITY_END_TIME = datetime.now().replace(hour=22, minute=0, second=0, microsecond=0)
STEP_COUNT_BASE = 0
SLEEP_START_TIME = datetime.now().replace(hour=22, minute=0, second=0, microsecond=0)
SLEEP_END_TIME = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0) + timedelta(days=1)
IDEAL_SLEEP_DURATION = 8  # hours
EXTREME_CONDITIONS_PROBABILITY = 0.01  # Probability of extreme condition per time interval
EXTREME_CONDITIONS_FREQUENCY = 0.1  # Probability of extreme condition occurring at all within a day

def simulate_step_count(current_step_count, speed, duration):
    """Accumulate step count based on walking speed and duration."""
    steps_per_minute = int(speed * 60)  # Convert speed to steps per minute
    return int(current_step_count + (steps_per_minute * duration))  # Ensure step count is an integer

def simulate_heartbeat(activity_speed, extreme_condition=False):
    base_heartbeat = 70  # Resting heart rate
    if extreme_condition:
        return np.random.randint(100, 200)  # Simulate very high or low heart rate
    if activity_speed == 0:
        return np.random.randint(base_heartbeat - 10, base_heartbeat + 10)
    elif activity_speed <= WALKING_SPEED_LOW:
        return np.random.randint(base_heartbeat + 10, base_heartbeat + 20)
    elif activity_speed <= WALKING_SPEED_MEDIUM:
        return np.random.randint(base_heartbeat + 20, base_heartbeat + 30)
    else:
        return np.random.randint(base_heartbeat + 30, base_heartbeat + 40)

def simulate_glucose_rate(activity_speed, meal_time, extreme_condition=False):
    base_glucose = 100  # mg/dL, average glucose level
    if extreme_condition:
        return np.random.uniform(150, 300)  # Simulate very high glucose levels
    if activity_speed > 0:
        glucose_rate = np.random.uniform(base_glucose - 10, base_glucose + 10)
    else:
        glucose_rate = np.random.uniform(base_glucose - 5, base_glucose + 20)
    
    if meal_time:
        glucose_rate += np.random.uniform(10, 30)  # Increase after meals
    
    return glucose_rate

def simulate_blood_pressure(activity_speed, extreme_condition=False):
    base_systolic = 120  # Average systolic BP
    base_diastolic = 80  # Average diastolic BP
    if extreme_condition:
        return (np.random.randint(180, 200), np.random.randint(120, 140))  # High BP
    if activity_speed > WALKING_SPEED_MEDIUM:
        systolic = np.random.randint(base_systolic + 10, base_systolic + 20)
        diastolic = np.random.randint(base_diastolic + 10, base_diastolic + 20)
    else:
        systolic = np.random.randint(base_systolic - 10, base_systolic + 10)
        diastolic = np.random.randint(base_diastolic - 10, base_diastolic + 10)
    
    return systolic, diastolic

def simulate_spO2(extreme_condition=False):
    if extreme_condition:
        return np.random.uniform(85, 90)  # Simulate low oxygen levels
    return np.random.uniform(95, 100)

def simulate_body_temperature(activity_speed, extreme_condition=False):
    base_temp = 36.5  # Average body temperature in Celsius
    if extreme_condition:
        return np.random.uniform(38, 40)  # High fever range
    if activity_speed > 0:
        return np.random.uniform(base_temp + 0.5, base_temp + 1.0)
    else:
        return np.random.uniform(base_temp - 0.5, base_temp + 0.5)

def simulate_calories_burned(activity_speed, duration):
    base_calories_per_hour = 100  # Calories burned at rest per hour
    return base_calories_per_hour * duration * (activity_speed / WALKING_SPEED_MEDIUM)

def simulate_hydration_level(current_time, extreme_condition=False):
    if extreme_condition:
        return np.random.uniform(60, 70)  # Lower hydration levels
    hour = current_time.hour
    if 6 <= hour < 12:
        return np.random.uniform(80, 90)  # Morning hydration
    elif 12 <= hour < 18:
        return np.random.uniform(70, 80)  # Afternoon hydration
    else:
        return np.random.uniform(65, 75)  # Evening hydration


def calculate_sleep_quality(sleep_duration):
    if sleep_duration < 6:
        return np.random.uniform(2, 4)  # Poor quality
    elif 6 <= sleep_duration <= 8:
        return np.random.uniform(5, 7)  # Fair quality
    else:
        return np.random.uniform(8, 10)  # Good quality

def get_activity_level():
    current_hour = datetime.now().hour
    if 6 <= current_hour < 8:  # Morning activity (e.g., exercise)
        return random.uniform(WALKING_SPEED_MEDIUM, WALKING_SPEED_HIGH)
    elif 8 <= current_hour < 12:  # Work hours
        return random.uniform(0, WALKING_SPEED_LOW)  # Mostly sedentary
    elif 12 <= current_hour < 13:  # Lunch break
        return random.uniform(WALKING_SPEED_LOW, WALKING_SPEED_MEDIUM)
    elif 13 <= current_hour < 17:  # Afternoon work
        return random.uniform(0, WALKING_SPEED_LOW)
    elif 17 <= current_hour < 19:  # Evening activity
        return random.uniform(WALKING_SPEED_MEDIUM, WALKING_SPEED_HIGH)
    else:  # Nighttime (preparing for bed)
        return random.uniform(0, WALKING_SPEED_LOW)

def generate_real_time_data(start_time, end_time, interval=60):
    current_time = start_time
    step_count = STEP_COUNT_BASE  # Initialize the base step count
    total_calories_burned = 0  # Initialize total calories burned
    total_sleep_duration = 0

    while current_time <= end_time:
        # Randomly introduce extreme conditions with a lower probability
        extreme_condition = random.random() < EXTREME_CONDITIONS_PROBABILITY and random.random() < EXTREME_CONDITIONS_FREQUENCY

        if SLEEP_START_TIME <= current_time <= SLEEP_END_TIME:
            # During sleep, no step count, simulate sleep metrics
            sleep_duration = (current_time - SLEEP_START_TIME).total_seconds() / 3600
            sleep_quality = calculate_sleep_quality(sleep_duration)
        else:
            # Determine activity level
            activity_speed = get_activity_level()
            duration = interval / 60  # Duration in hours

            if activity_speed > 0:  # Only accumulate steps if there is activity
                step_count = simulate_step_count(step_count, activity_speed, duration)

            # Simulate other health metrics based on activity level and extreme conditions
            heartbeat = simulate_heartbeat(activity_speed, extreme_condition)
            meal_time = random.choice([True, False])  # Randomly simulate meal times
            glucose_rate = simulate_glucose_rate(activity_speed, meal_time, extreme_condition)
            systolic, diastolic = simulate_blood_pressure(activity_speed, extreme_condition)
            spO2 = simulate_spO2(extreme_condition)
            body_temperature = simulate_body_temperature(activity_speed, extreme_condition)
            calories_burned = simulate_calories_burned(activity_speed, duration)

            # Accumulate total calories burned
            total_calories_burned += calories_burned

            hydration_level = simulate_hydration_level(current_time, extreme_condition)
            sleep_quality = calculate_sleep_quality(total_sleep_duration)

        # Create a DataFrame for the record
        data = pd.DataFrame([{
            'Timestamp': current_time.isoformat(),
            'Step_Count': step_count,
            'Heartbeat': heartbeat,
            'Glucose_Rate': glucose_rate,
            'Blood_Pressure_Systolic': systolic,
            'Blood_Pressure_Diastolic': diastolic,
            'SpO2': spO2,
            'Body_Temperature': body_temperature,
            'Calories_Burned': total_calories_burned,  # Use total calories burned
            'Hydration_Level': hydration_level,
            'Sleep_Quality': sleep_quality
        }])
        
        dict_data = data.to_dict(orient='records')
        new_data = json.dumps(dict_data)  # Serialize the data to a JSON string
        print(data)  # Output data, you can replace this with streaming to a service
        send_to_firehose(new_data)
        
        # Increment time
        current_time += timedelta(minutes=interval)

        # Sleep for the interval before generating the next record
        time.sleep(interval)



# Example usage: Simulate data from 6 AM to 10 PM with 1-minute intervals
if __name__ == "__main__":
    generate_real_time_data(ACTIVITY_START_TIME, ACTIVITY_END_TIME, interval=5)





