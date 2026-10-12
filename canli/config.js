// Firebase web ayarı (gizli değildir; güvenliği Firestore kuralları sağlar)
window.FB_CONFIG = (location.hostname === "localhost" || location.hostname === "127.0.0.1")
  ? { apiKey: "demo-key", authDomain: "demo-lam.firebaseapp.com", projectId: "demo-lam" }
  : {
      apiKey: "AIzaSyAByR-tIX9dIPyeQu81RjGbaPlNtWfzx7Q",
      authDomain: "lam-basinda.firebaseapp.com",
      projectId: "lam-basinda",
      storageBucket: "lam-basinda.firebasestorage.app",
      messagingSenderId: "400276010201",
      appId: "1:400276010201:web:73fb1226eabaadd0737ac8"
    };

// Perde hesabı: Firebase Authentication → Users içinde e-posta/şifre ile açılmış sabit hesap.
// Perde sayfasında yalnız şifre sorulur; aynı e-posta firestore.rules içindeki perdeListesi() ile eşleşmeli.
window.PERDE_EPOSTA = "perde@lam-basinda.app";
