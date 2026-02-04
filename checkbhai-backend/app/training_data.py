"""
Training dataset for CheckBhai AI scam detection model
Contains 50+ labeled examples across 5 categories with multilingual support
"""

TRAINING_DATA = [
    # Job Scams - English
    {
        "text": "Congratulations! You've been selected for a high-paying job at Google. Send $500 for visa processing immediately to secure your position.",
        "label": "Scam",
        "category": "Job",
        "urgency": True,
        "overpromise": True,
        "payment_method": "advance_fee"
    },
    {
        "text": "Work from home and earn $5000/month! No experience needed. Just pay $200 registration fee to start earning today!",
        "label": "Scam",
        "category": "Job",
        "urgency": True,
        "overpromise": True,
        "payment_method": "registration_fee"
    },
    {
        "text": "Thank you for applying to our Software Engineer position. We'd like to schedule an interview next week. Please confirm your availability.",
        "label": "Legit",
        "category": "Job",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    
    # Job Scams - Bangla/Banglish
    {
        "text": "Apni selected hoyechen! Dubai job paben, salary 80000 taka. Taka pathao 15000, visa processing er jonno. Taratari koren!",
        "label": "Scam",
        "category": "Job",
        "urgency": True,
        "overpromise": True,
        "payment_method": "visa_fee"
    },
    {
        "text": "আপনি আমাদের কোম্পানিতে একাউন্ট্যান্ট পদের জন্য নির্বাচিত হয়েছেন। আগামীকাল সাক্ষাৎকারের জন্য আসবেন।",
        "label": "Legit",
        "category": "Job",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Ghor bose kajo koren, mase 50000 income! Sudhu 3000 taka diye registration koren. Limited seats!",
        "label": "Scam",
        "category": "Job",
        "urgency": True,
        "overpromise": True,
        "payment_method": "registration_fee"
    },
    
    # Agent Scams - English
    {
        "text": "I guarantee 100% visa approval for USA. Pay me 500000 BDT and your visa will be processed in 2 weeks guaranteed!",
        "label": "Scam",
        "category": "Agent",
        "urgency": True,
        "overpromise": True,
        "payment_method": "upfront_payment"
    },
    {
        "text": "Canada student visa processing: We charge 150000 BDT fee after visa approval. Initial consultation is free.",
        "label": "Legit",
        "category": "Agent",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "URGENT! Only 2 slots left for Australia work visa. 100% guarantee! Pay 600000 taka within 24 hours or lose this opportunity!",
        "label": "Scam",
        "category": "Agent",
        "urgency": True,
        "overpromise": True,
        "payment_method": "upfront_payment"
    },
    
    # Agent Scams - Bangla/Banglish
    {
        "text": "Singapore visa 100% confirm! Ami guarantee dichchi. Taka advance den 400000. Visa na hole taka ferot.",
        "label": "Scam",
        "category": "Agent",
        "urgency": False,
        "overpromise": True,
        "payment_method": "upfront_payment"
    },
    {
        "text": "আমরা ভিসা প্রসেসিং সহায়তা করি। ফি ভিসা পাওয়ার পরে নেওয়া হবে। প্রথম পরামর্শ বিনামূল্যে।",
        "label": "Legit",
        "category": "Agent",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Ajo rat 12 tar moddhe taka pathale Malaysia visa confirm! Guarantee 100%! Taratari koren slots sesh!",
        "label": "Scam",
        "category": "Agent",
        "urgency": True,
        "overpromise": True,
        "payment_method": "upfront_payment"
    },
    
    # Seller Scams - English
    {
        "text": "Brand new iPhone 15 Pro Max only 15000 BDT! Limited stock! Send advance payment via Bkash now!",
        "label": "Scam",
        "category": "Seller",
        "urgency": True,
        "overpromise": True,
        "payment_method": "bkash_advance"
    },
    {
        "text": "Selling my used iPhone 12 for 45000 BDT. Cash on delivery available. Can meet at safe public location.",
        "label": "Legit",
        "category": "Seller",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "MacBook Pro M3 original, only 25000 taka! But you must pay full amount today via Rocket. No refund policy.",
        "label": "Scam",
        "category": "Seller",
        "urgency": True,
        "overpromise": True,
        "payment_method": "rocket_advance"
    },
    
    # Seller Scams - Bangla/Banglish
    {
        "text": "Samsung Galaxy S24 Ultra original, dam matro 18000 taka! Ajo advance Bkash pathale delivery kaal! Taratari!",
        "label": "Scam",
        "category": "Seller",
        "urgency": True,
        "overpromise": True,
        "payment_method": "bkash_advance"
    },
    {
        "text": "পুরাতন ল্যাপটপ বিক্রয়। দাম ৩০০০০ টাকা। হাতে হাতে লেনদেন করব উত্তরার কাছে।",
        "label": "Legit",
        "category": "Seller",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "PlayStation 5 brand new, 12000 taka only! Akhon Bkash na korle stock sesh! Only 1 piece left!",
        "label": "Scam",
        "category": "Seller",
        "urgency": True,
        "overpromise": True,
        "payment_method": "bkash_advance"
    },
    
    # Investment Scams - English
    {
        "text": "Invest 50000 BDT today and get 200000 BDT in 30 days! Guaranteed returns! Limited slots available!",
        "label": "Scam",
        "category": "Investment",
        "urgency": True,
        "overpromise": True,
        "payment_method": "investment"
    },
    {
        "text": "Our mutual fund offers 8-12% annual returns based on market performance. Minimum investment 10000 BDT. SECP registered.",
        "label": "Legit",
        "category": "Investment",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Join our pyramid scheme! Invest 20000 and recruit 5 friends. You'll make 500000 in 1 month guaranteed!",
        "label": "Scam",
        "category": "Investment",
        "urgency": True,
        "overpromise": True,
        "payment_method": "pyramid"
    },
    
    # Investment Scams - Bangla/Banglish
    {
        "text": "10000 taka invest koren, 1 mas pore 50000 taka paben! 100% guarantee! Amar sathe join korun!",
        "label": "Scam",
        "category": "Investment",
        "urgency": True,
        "overpromise": True,
        "payment_method": "investment"
    },
    {
        "text": "আমাদের কোম্পানি বছরে ১০-১৫% রিটার্ন দেয়। ঝুঁকি থাকতে পারে। SECP অনুমোদিত।",
        "label": "Legit",
        "category": "Investment",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Bitcoin trading group join koren! 25000 taka dile 1 lakh guaranteed week e! Miss korben na!",
        "label": "Scam",
        "category": "Investment",
        "urgency": True,
        "overpromise": True,
        "payment_method": "crypto_scam"
    },
    
    # Course Scams - English
    {
        "text": "Become a certified data scientist in 7 days! Pay 15000 BDT now and get guaranteed job placement at Google!",
        "label": "Scam",
        "category": "Course",
        "urgency": True,
        "overpromise": True,
        "payment_method": "course_fee"
    },
    {
        "text": "Our 6-month web development bootcamp costs 50000 BDT. Industry-recognized certificate upon completion. No job guarantee.",
        "label": "Legit",
        "category": "Course",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Last day to enroll! Digital marketing course - become expert in 3 days! Guaranteed 50000 BDT/month income! Pay 8000 now!",
        "label": "Scam",
        "category": "Course",
        "urgency": True,
        "overpromise": True,
        "payment_method": "course_fee"
    },
    
    # Course Scams - Bangla/Banglish
    {
        "text": "Freelancing course - 5 din e expert hoye jan! Guarantee mase 1 lakh income! Taka pathao 12000, shuru hobe ajo!",
        "label": "Scam",
        "category": "Course",
        "urgency": True,
        "overpromise": True,
        "payment_method": "course_fee"
    },
    {
        "text": "আমাদের ৪ মাসের গ্রাফিক ডিজাইন কোর্স। ফি ২৫০০০ টাকা। সার্টিফিকেট দেওয়া হবে।",
        "label": "Legit",
        "category": "Course",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Ajo enroll na korle miss! AI course - 1 week e expert! Google Microsoft job 100% guarantee! Fee 20000!",
        "label": "Scam",
        "category": "Course",
        "urgency": True,
        "overpromise": True,
        "payment_method": "course_fee"
    },
    
    # Additional Mixed Examples
    {
        "text": "Ami apnar account verify korte chai. Apnar Bkash PIN number amake den taratari.",
        "label": "Scam",
        "category": "Phishing",
        "urgency": True,
        "overpromise": False,
        "payment_method": "phishing"
    },
    {
        "text": "Your OTP for transaction is 123456. Do not share this with anyone.",
        "label": "Legit",
        "category": "Banking",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Apni lottery jitechen 10 lakh taka! Claim korte 5000 taka processing fee pathao!",
        "label": "Scam",
        "category": "Lottery",
        "urgency": True,
        "overpromise": True,
        "payment_method": "advance_fee"
    },
    {
        "text": "আপনার অ্যাকাউন্ট সিকিউরিটির জন্য পাসওয়ার্ড পরিবর্তন করুন। আমাদের অফিশিয়াল ওয়েবসাইট ব্যবহার করুন।",
        "label": "Legit",
        "category": "Banking",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Free loan approve hoyeche 5 lakh taka! Sudhu 10000 taka advance fee den, tarpor loan paben!",
        "label": "Scam",
        "category": "Loan",
        "urgency": True,
        "overpromise": True,
        "payment_method": "advance_fee"
    },
    {
        "text": "আমাদের ব্যাংক থেকে ঋণের জন্য আবেদন করুন। সুদের হার ১২%। ডকুমেন্ট যাচাই করে অনুমোদন দেওয়া হবে।",
        "label": "Legit",
        "category": "Loan",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Amazon gift card 5000 taka matro 500 taka te! Limited offer! Bkash koren akhuni!",
        "label": "Scam",
        "category": "Seller",
        "urgency": True,
        "overpromise": True,
        "payment_method": "bkash_advance"
    },
    {
        "text": "We are hiring for customer support. Salary 25000 BDT/month. Interview scheduled for Monday 10 AM.",
        "label": "Legit",
        "category": "Job",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Corona vaccine available! Pay 2000 taka per dose advance. Limited stock, book now!",
        "label": "Scam",
        "category": "Medical",
        "urgency": True,
        "overpromise": True,
        "payment_method": "advance_payment"
    },
    {
        "text": "Free COVID-19 vaccination camp on Saturday at Community Center. Bring your NID card.",
        "label": "Legit",
        "category": "Medical",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Tumi lottery jiteche 50 lakh! Claim korte amar sathe call koro ekhon! Taratari na korle expire!",
        "label": "Scam",
        "category": "Lottery",
        "urgency": True,
        "overpromise": True,
        "payment_method": "phishing"
    },
    {
        "text": "Your parcel is ready for delivery. Please pay 150 BDT delivery charge via cash on delivery.",
        "label": "Legit",
        "category": "Delivery",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Facebook account deactivate hoye jabe! Link e click kore password verify koro ekhoni!",
        "label": "Scam",
        "category": "Phishing",
        "urgency": True,
        "overpromise": False,
        "payment_method": "phishing"
    },
    {
        "text": "আপনার পণ্য ডেলিভারি দিতে আসব আগামীকাল। ঠিকানা কনফার্ম করুন।",
        "label": "Legit",
        "category": "Delivery",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Scholarship available for students! Full free education in USA! Just send 50000 BDT processing fee!",
        "label": "Scam",
        "category": "Education",
        "urgency": True,
        "overpromise": True,
        "payment_method": "processing_fee"
    },
    {
        "text": "Apply for our scholarship program. Merit-based selection. Application deadline is next month. No fees required.",
        "label": "Legit",
        "category": "Education",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    },
    {
        "text": "Gold rate 50% off! 22k gold 500 taka per vori! Order koren ekhoni Rocket e taka pathiye!",
        "label": "Scam",
        "category": "Seller",
        "urgency": True,
        "overpromise": True,
        "payment_method": "rocket_advance"
    },
    {
        "text": "আমরা স্বর্ণের গহনা তৈরি করি। দোকানে এসে দেখে যান। দাম বাজার অনুযায়ী।",
        "label": "Legit",
        "category": "Seller",
        "urgency": False,
        "overpromise": False,
        "payment_method": None
    }
]

def get_training_data():
    """Returns the complete training dataset"""
    return TRAINING_DATA

def get_scam_examples():
    """Returns only scam examples"""
    return [d for d in TRAINING_DATA if d['label'] == 'Scam']

def get_legit_examples():
    """Returns only legitimate examples"""
    return [d for d in TRAINING_DATA if d['label'] == 'Legit']

def get_by_category(category):
    """Returns examples filtered by category"""
    return [d for d in TRAINING_DATA if d['category'] == category]
