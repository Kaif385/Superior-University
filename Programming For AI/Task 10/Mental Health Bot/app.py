from flask import Flask, render_template, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections


app = Flask(__name__)

pairs = [    
[r"(?i).*(hi|hello|hey|holla|hola|greetings)", ["Hello! I am here to listen. How are you feeling today?", "Hi there! I am a supportive AI. What's on your mind?"]],
    [r"(?i).*(morning|afternoon|evening)", ["Good day! I hope you are doing well. How can I help?"]],
    [r"(?i).*(bye|goodbye|see you|later|exit|quit)", ["Goodbye! Remember to be kind to yourself today.", "Take care. I'm here whenever you need to chat."]],
    [r"(?i).*(thank|thanks|appreciate)", ["You are very welcome. Take care of yourself!", "No problem! I'm here if you need me."]],
    [r"(?i).*(who are you|your name|what are you)", ["I am a mental health support chatbot created for a student assignment."]],
    [r"(?i).*(human|robot|ai|bot)", ["I am a robot (AI), but I am programmed to be supportive and empathetic."]],
    [r"(?i).*(real|alive|feelings)", ["I am code and data, but I am here to simulate understanding and support."]],
    [r"(?i).*(where do you live|location)", ["I live on a server, but I am right here on your screen whenever you need me."]],
    [r"(?i).*(sick|not feeling well|feeling unwell|not well|wel|ill|pain)", ["I am sorry to hear that. Have you been feeling this way for long? You might want to rest or see a doctor if it persists."]],
    [r"(?i).*(kill myself|suicide|die|end it|hurt myself|death)", ["Please stop. You are not alone. If you are in immediate danger, please call your local emergency number or a suicide hotline immediately. Your life has value."]],
    [r"(?i).*(sad|depressed|unhappy|down|low|blue)", ["I'm sorry to hear that. Sadness is a valid emotion. Do you want to talk about what is making you feel this way?", "It is okay to feel sad sometimes. Be gentle with yourself."]],
    [r"(?i).*(cry|crying|tears|weeping)", ["It is okay to cry. Letting it out can be a healthy release. I am here with you."]],
    [r"(?i).*(lonely|alone|isolated|no friends)", ["I know loneliness can be heavy. Even if I am a bot, I am here to listen. Have you tried reaching out to a friend or family member today?"]],
    [r"(?i).*(empty|numb|nothing|void)", ["Feeling empty can be a sign of depression or burnout. Doing small things that usually bring you joy might help spark some feeling."]],
    [r"(?i).*(anxious|worried|nervous|scared|fear|panic|anxiety)", ["Anxiety can be tough. Try this grounding technique: Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, and 1 you taste."]],
    [r"(?i).*(stress|stressed|pressure|tension)", ["Stress is normal, but too much can be overwhelming. Try breaking your tasks into tiny steps. Just do one small thing at a time."]],
    [r"(?i).*(overwhelmed|too much)", ["Take a deep breath. You don't have to solve everything today. What is the one most important thing to do right now?"]],
    [r"(?i).*(panic attack|cant breathe)", ["If you are having a panic attack, focus on your breathing. Breathe in slowly... and out slowly. Remind yourself: 'This will pass'."]],
    [r"(?i).*(angry|rage|mad|furious|hate)", ["Anger is a strong emotion. It often protects us from hurt. Taking deep breaths or squeezing a stress ball might help safely release that energy."]],
    [r"(?i).*(annoyed|irritated)", ["It sounds like you are frustrated. It's okay to vent here. What is bothering you?"]],
    [r"(?i).*(worthless|useless|waste)", ["You are not worthless. Depression often lies to us. You have value just by being here."]],
    [r"(?i).*(hate myself|loathe myself)", ["I am really sorry you feel that way. You deserve support and kindness, especially from yourself."]],
    [r"(?i).*(failure|fail|failing)", ["You are not a failure. You are a person learning and growing. Mistakes are just part of the process."]],
    [r"(?i).*(ugly|fat|look bad|body image)", ["Beauty is subjective. Try to focus on what your body allows you to do (like breathe, move, feel) rather than just how it looks."]],
    [r"(?i).*(guilty|shame|ashamed|mistake)", ["Everyone makes mistakes. Guilt shows you care, but holding onto it doesn't help. Can you forgive yourself?"]],
    [r"(?i).*(shy|quiet|introvert)", ["Being shy is a personality trait, not a flaw. You don't have to be the loudest person in the room to have value."]],
    [r"(?i).*(confident|confidence)", ["Confidence is a muscle. Fake it until you make it. Stand tall, speak clearly, and be kind to yourself."]],
    [r"(?i).*(weird|strange|freak)", ["Everyone is weird in their own way. That is what makes people interesting. Embrace your uniqueness."]],
    [r"(?i).*(nobody understands|misunderstood)", ["It can feel that way. But with 7 billion people, there is someone who understands. Keep looking for your tribe."]],
    [r"(?i).*(sleep|insomnia|awake|tired|exhausted|burnout|fatigue)", ["Sleep is so important. Try avoiding screens for an hour before bed and keeping your room cool and dark."]],
    [r"(?i).*(bored|boredom)", ["Boredom can be an opportunity. Read a book, draw, take a walk, or learn a new skill."]],
    [r"(?i).*(motivation|motivated|lazy|procrastinating)", ["Action often comes before motivation. Try doing a task for just 5 minutes. You might find it easier to keep going."]],
    [r"(?i).*(self care|relax)", ["Self-care ideas: Take a bath, read a book, go for a walk, drink water, say no to plans, or sleep early."]],
    [r"(?i).*(friend|relationship|breakup|heartbreak|ex)", ["Relationships are hard. If you are going through a breakup, allow yourself to grieve. It takes time to heal."]],
    [r"(?i).*(social anxiety|people|crowd)", ["Social anxiety is common. In social situations, try focusing on the other person rather than your own internal worries."]],
    [r"(?i).*(help a friend|friend is sad)", ["Listen without judging. You don't have to fix their problems; just being there is often enough."]],
    [r"(?i).*(jealous|envy)", ["Jealousy is natural. It usually points to something we want for ourselves. Can you turn that into a goal?"]],
    [r"(?i).*(depression|depressed)", ["Depression is a common medical illness that negatively affects how you feel, the way you think, and how you act."]],
    [r"(?i).*(anxiety disorder|gad)", ["Anxiety is your body's natural response to stress. If it is affecting your life, professional help is very effective."]],
    [r"(?i).*(therapy|counseling|therapist)", ["Therapy is a process of talking to a trained professional to understand your feelings and learn coping skills."]],
    [r"(?i).*(medication|pills)", ["Medication can be very helpful for many people. It is best to discuss this with a doctor or psychiatrist."]],
    [r"(?i).*(ptsd|trauma)", ["PTSD is a reaction to trauma. Grounding techniques and professional therapy are very effective treatments."]],
    [r"(?i).*(bipolar|mood swings)", ["Bipolar disorder involves mood swings. Sticking to a routine and medication plan is usually very important."]],
    [r"(?i).*(ocd|obsessive)", ["OCD involves unwanted thoughts and repetitive behaviors. Exposure and Response Prevention (ERP) therapy is often helpful."]],
    [r"(?i).*(voices|hallucinate)", ["Hearing voices can be distressing. It is important to see a doctor to understand why this is happening."]],
    [r"(?i).*(mindfulness|present)", ["Mindfulness is the ability to be fully present in the moment. Try focusing entirely on your breath for one minute."]],
    [r"(?i).*(grounding|reality)", ["5-4-3-2-1 technique: Acknowledge 5 things you see, 4 you can touch, 3 you hear, 2 you can smell, and 1 you can taste."]],
    [r"(?i).*(breathe|breathing)", ["Box breathing: Inhale 4s, Hold 4s, Exhale 4s, Hold 4s. Repeat."]],
    [r"(?i).*(affirmation|positive)", ["Try saying: 'I am enough', 'I am doing my best', 'I deserve peace'."]],
    [r"(?i).*(hopeless|no hope)", ["Hopelessness is a symptom, not a reality. Situations change. Please hold on and talk to someone."]],
    [r"(?i).*(why me|unfair)", ["Life can be unfair. It is valid to feel frustrated. Focus on what you can control, even if it's just your next breath."]],
    [r"(?i).*(confused|lost)", ["Confusion is okay. Write down what is confusing you. Seeing it on paper might help clarify things."]],
    [r"(?i).*(joke|laugh|smile)", ["Why did the scarecrow win an award? Because he was outstanding in his field!"]],
    [r"(?i).*(ok|okay|k|fine|alright|good)", ["I'm glad to hear that. How else can I support you today?"]],
    [r"(.*)", ["I am listening. Please go on.", "Can you tell me more about that?", "How does that make you feel?"]]
]
chatbot = Chat(pairs, reflections)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def chat():
    user_input = request.form.get('msg')
    if not user_input:
        return jsonify({'response': "Please type a message."})


    elif user_input.lower() == "bye":
        return jsonify({'response': "Goodbye! Take care."})

    else:
        response = chatbot.respond(user_input)
        if response:
            return jsonify({'response': response})
        else:
            return jsonify({'response': "Sorry! I'm unable to respond to that."})


app.run(debug=True)



