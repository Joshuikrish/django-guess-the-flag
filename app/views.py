from django.shortcuts import render, redirect
from .models import Flag
import random
import json
import os

def home(request):
    flags = list(Flag.objects.all())
    selected_flag = None
    feedback = None
    score = request.session.get('score', 0)
    status = False
    shown_flags = request.session.get('shown_flags', [])

    # Load the countries.json file to get the country names
    json_file_path = os.path.join(os.path.dirname(__file__), 'countries.json')
    with open(json_file_path, 'r', encoding='utf-8') as f:
        countries = json.load(f)

    if request.method == 'POST':
        if 'reset' in request.POST:
            request.session['score'] = 0
            request.session['shown_flags'] = []
            return redirect('home')

        country_name = request.POST.get('country').strip().lower()
        flag_id = request.POST.get('flag_id')
        try:
            selected_flag = Flag.objects.get(id=flag_id)
            # Find the key (shortcut) for the given country name
            correct_key = None
            for key, value in countries.items():
                if value.lower() == country_name:
                    correct_key = key.lower()
                    break

            if correct_key and selected_flag.name.lower() == correct_key:
                feedback = "Correct! Well done!"
                status = True
                score += 1
            else:
                correct_country_name = countries.get(selected_flag.name.upper(), "Unknown")
                feedback = f"Incorrect! The correct answer was {correct_country_name}."
                status = False
                score -= 1
        except Flag.DoesNotExist:
            feedback = "Flag not found."
        request.session['score'] = score

        # Ensure shown_flags is a list of integers
        shown_flags = [int(flag_id) for flag_id in shown_flags]

        # Add the current flag to shown_flags
        if selected_flag and selected_flag.id not in shown_flags:
            shown_flags.append(selected_flag.id)
            request.session['shown_flags'] = shown_flags

    # Check if all flags have been shown
    if len(shown_flags) >= len(flags):
        feedback = "Congratulations! You've completed the quiz."
        selected_flag = None
    else:
        # Select a new flag that hasn't been shown yet
        remaining_flags = [flag for flag in flags if flag.id not in shown_flags]
        if remaining_flags:
            selected_flag = random.choice(remaining_flags)

    data = {
        'flags': flags,
        'selected_flag': selected_flag,
        'feedback': feedback,
        'status': status,
        'score': score,
    }
    return render(request, 'index.html', data)