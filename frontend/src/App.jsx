import React, { useState, useEffect } from 'react';
import api from './api';
import './App.css';

function App() {
  const [isAuth, setIsAuth] = useState(false);
  const [user, setUser] = useState(null);
  const [phone, setPhone] = useState('');
  const [name, setName] = useState('');
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState('en');
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api.get('/api/me').then(res => {
        setUser(res.data);
        setIsAuth(true);
      }).catch(() => {
        localStorage.removeItem('token');
      });
    }
  }, []);

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.post('/api/register', null, { params: { phone, name } });
      localStorage.setItem('token', data.access_token);
      setUser(data.user);
      setIsAuth(true);
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || 'Registration failed'));
    }
  };

  const handleCheck = async (e) => {
    e.preventDefault();
    if (!text.trim()) {
      alert(language === 'en' ? 'Please enter text to check' : 'অনুগ্রহ করে টেক্সট লিখুন');
      return;
    }

    setLoading(true);
    try {
      const { data } = await api.post('/api/check', null, { params: { text } });
      setResult(data);
      setText('');
      
      // Refresh user credits
      const userRes = await api.get('/api/me');
      setUser(userRes.data);
    } catch (error) {
      if (error.response?.status === 402) {
        alert(language === 'en' ? 'No credits remaining!' : 'ক্রেডিট শেষ!');
      } else {
        alert('Error: ' + (error.response?.data?.detail || 'Check failed'));
      }
    }
    setLoading(false);
  };

  const handleFeedback = async (checkId, feedback) => {
    await api.post('/api/feedback', null, { params: { check_id: checkId, feedback } });
    alert(language === 'en' ? 'Thank you for feedback!' : 'ফিডব্যাক এর জন্য ধন্যবাদ!');
    setResult(null);
  };

  const text_data = {
    en: {
      title: 'CheckBhai',
      tagline: 'Scam Detection Platform',
      enterText: 'Enter message, offer, or post to check',
      checkBtn: 'Check for Scam',
      checking: 'Analyzing...',
      credits: 'Credits',
      riskLevel: 'Risk Level',
      redFlags: 'Red Flags Detected',
      analysis: 'Analysis',
      wasAccurate: 'Was this accurate?',
      yes: 'Yes',
      no: 'No',
      checkAnother: 'Check Another',
      examples: 'Examples to Try',
      example1: 'Send 10k Bkash now, get 50k guaranteed!',
      example2: 'Work from home, earn 2 lakh/month. Registration 5k.',
      example3: 'We are hiring. Free application.',
      phone: 'Phone Number',
      name: 'Your Name',
      start: 'Start',
      logout: 'Logout'
    },
    bn: {
      title: 'চেকভাই',
      tagline: 'স্ক্যাম ডিটেকশন প্ল্যাটফর্ম',
      enterText: 'মেসেজ, অফার বা পোস্ট লিখুন',
      checkBtn: 'স্ক্যাম চেক করুন',
      checking: 'বিশ্লেষণ চলছে...',
      credits: 'ক্রেডিট',
      riskLevel: 'ঝুঁকির মাত্রা',
      redFlags: 'সনাক্তকৃত সমস্যা',
      analysis: 'বিশ্লেষণ',
      wasAccurate: 'এটি কি সঠিক ছিল?',
      yes: 'হ্যাঁ',
      no: 'না',
      checkAnother: 'আরেকটি চেক করুন',
      examples: 'উদাহরণ',
      example1: '১০ হাজার বিকাশ করুন, ৫০ হাজার পাবেন!',
      example2: 'ঘরে বসে কাজ, মাসে ২ লাখ আয়। রেজিস্ট্রেশন ৫ হাজার।',
      example3: 'আমরা নিয়োগ দিচ্ছি। আবেদন ফ্রি।',
      phone: 'ফোন নম্বর',
      name: 'আপনার নাম',
      start: 'শুরু করুন',
      logout: 'লগআউট'
    }
  };

  const t = text_data[language];

  if (!isAuth) {
    return (
      <div className="app">
        <div className="auth-container">
          <div className="logo">🔍</div>
          <h1>{t.title}</h1>
          <p className="tagline">{t.tagline}</p>
          
          <form onSubmit={handleRegister} className="auth-form">
            <input
              type="tel"
              placeholder={t.phone}
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder={t.name}
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
            <button type="submit">{t.start}</button>
          </form>

          <button className="lang-toggle" onClick={() => setLanguage(language === 'en' ? 'bn' : 'en')}>
            {language === 'en' ? 'বাংলা' : 'English'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header>
        <div className="header-content">
          <div>
            <h1>🔍 {t.title}</h1>
            <p className="user-info">{user?.name} • {t.credits}: {user?.credits || 0}</p>
          </div>
          <div className="header-actions">
            <button className="lang-toggle" onClick={() => setLanguage(language === 'en' ? 'bn' : 'en')}>
              {language === 'en' ? 'বাংলা' : 'English'}
            </button>
            <button className="logout-btn" onClick={() => { localStorage.removeItem('token'); setIsAuth(false); }}>
              {t.logout}
            </button>
          </div>
        </div>
      </header>

      <main>
        {!result ? (
          <div className="check-container">
            <div className="mascot">👮</div>
            <h2>{t.tagline}</h2>

            <form onSubmit={handleCheck} className="check-form">
              <textarea
                placeholder={t.enterText}
                value={text}
                onChange={(e) => setText(e.target.value)}
                rows={6}
                disabled={loading}
              />
              <button type="submit" disabled={loading} className="check-btn">
                {loading ? t.checking : t.checkBtn}
              </button>
            </form>

            <div className="examples">
              <p className="examples-title">{t.examples}:</p>
              <button className="example-btn" onClick={() => setText(t.example1)}>"{t.example1}"</button>
              <button className="example-btn" onClick={() => setText(t.example2)}>"{t.example2}"</button>
              <button className="example-btn" onClick={() => setText(t.example3)}>"{t.example3}"</button>
            </div>
          </div>
        ) : (
          <div className="result-container">
            <div className={`risk-badge risk-${result.risk_level}`}>
              {t.riskLevel}: {result.risk_level.toUpperCase()}
              <div className="risk-score">{result.risk_score}/100</div>
            </div>

            <div className="result-section">
              <h3>📋 {t.analysis}</h3>
              <p className="analysis-text">{result.analysis}</p>
            </div>

            {result.red_flags && result.red_flags.length > 0 && (
              <div className="result-section">
                <h3>🚩 {t.redFlags}</h3>
                <ul className="red-flags-list">
                  {result.red_flags.map((flag, idx) => (
                    <li key={idx}>⚠️ {flag}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="feedback-section">
              <p>{t.wasAccurate}</p>
              <div className="feedback-btns">
                <button onClick={() => handleFeedback(result.id, 'accurate')} className="feedback-btn yes">
                  👍 {t.yes}
                </button>
                <button onClick={() => handleFeedback(result.id, 'inaccurate')} className="feedback-btn no">
                  👎 {t.no}
                </button>
              </div>
            </div>

            <button onClick={() => setResult(null)} className="check-another-btn">
              {t.checkAnother}
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
