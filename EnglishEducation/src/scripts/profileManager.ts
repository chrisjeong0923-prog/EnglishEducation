import { APP_CONFIG } from '../config';

export interface UserProfile {
  id: string; // Unique profile identifier
  nickname: string;
  avatar: string; // Emoji character or label
  grade: string;   // 'grade3' | 'grade4' | 'grade5' | 'grade6'
  learnedWords: string[]; // List of words marked as learned
  quizScores: Record<string, number>; // quizTitle -> high score percentage
  listeningScores: Record<number, number>; // exerciseId -> high score accuracy percentage
}

export interface BadgeDefinition {
  id: string;
  nameEn: string;
  nameKh: string;
  descEn: string;
  descKh: string;
  icon: string;
}

export const BADGES: BadgeDefinition[] = [
  {
    id: "vocab_novice",
    nameEn: "Word Explorer",
    nameKh: "អ្នករុករកពាក្យ",
    descEn: "Mark at least 1 word as learned!",
    descKh: "កត់ចំណាំពាក្យយ៉ាងតិច ១ ថារៀនរួច!",
    icon: "🌱"
  },
  {
    id: "vocab_master",
    nameEn: "Vocabulary King",
    nameKh: "ស្តេចវាក្យសព្ទ",
    descEn: "Mark at least 8 words as learned!",
    descKh: "កត់ចំណាំពាក្យយ៉ាងតិច ៨ ថារៀនរួច!",
    icon: "👑"
  },
  {
    id: "quiz_champ",
    nameEn: "Grammar Master",
    nameKh: "កំពូលវេយ្យាករណ៍",
    descEn: "Score 100% on any grammar quiz!",
    descKh: "ទទួលបានពិន្ទុ ១០០% លើតេស្តសាកល្បងណាមួយ!",
    icon: "🏆"
  },
  {
    id: "listening_pro",
    nameEn: "Super Ears",
    nameKh: "ត្រចៀកទិព្វ",
    descEn: "Get 90% or higher accuracy on any listening exercise!",
    descKh: "ទទួលបានភាពត្រឹមត្រូវ ៩០% ឬខ្ពស់ជាងនេះលើការស្តាប់!",
    icon: "🐰"
  },
  {
    id: "star_collector",
    nameEn: "Star Collector",
    nameKh: "អ្នកប្រមូលផ្កាយ",
    descEn: "Collect 10 or more stars!",
    descKh: "ប្រមូលផ្កាយឱ្យបាន ១០ ឬច្រើនជាងនេះ!",
    icon: "⭐"
  },
  {
    id: "super_scholar",
    nameEn: "Super Scholar",
    nameKh: "កំពូលអ្នកប្រាជ្ញ",
    descEn: "Complete at least one word, one quiz, and one listening task!",
    descKh: "បំពេញយ៉ាងហោចណាស់ពាក្យសិក្សា១ តេស្ត១ និងការស្តាប់១!",
    icon: "🎓"
  }
];

const LOCAL_STORAGE_KEY_ACTIVE = "kids_edu_active_profile_id";
const LOCAL_STORAGE_KEY_PROFILES = "kids_edu_profiles";

// Helper to determine if we are in the browser
const isBrowser = () => typeof window !== "undefined";

export const profileManager = {
  // Migrates old single profile to new multi-profile structure
  migrateLegacyIfNeeded(): void {
    if (!isBrowser()) return;
    const legacyKey = "kids_edu_profile";
    const legacyData = localStorage.getItem(legacyKey);
    const currentProfiles = localStorage.getItem(LOCAL_STORAGE_KEY_PROFILES);

    if (legacyData && !currentProfiles) {
      try {
        const parsed = JSON.parse(legacyData);
        const uniqueId = "profile_" + Date.now();
        const migratedProfile: UserProfile = {
          id: uniqueId,
          nickname: parsed.nickname || "Young Learner",
          avatar: parsed.avatar || "🐼",
          grade: parsed.grade || "grade3",
          learnedWords: Array.isArray(parsed.learnedWords) ? parsed.learnedWords : [],
          quizScores: parsed.quizScores || {},
          listeningScores: parsed.listeningScores || {}
        };
        
        const profilesObj = { [uniqueId]: migratedProfile };
        localStorage.setItem(LOCAL_STORAGE_KEY_PROFILES, JSON.stringify(profilesObj));
        localStorage.setItem(LOCAL_STORAGE_KEY_ACTIVE, uniqueId);
        
        // Remove legacy key
        localStorage.removeItem(legacyKey);
      } catch (e) {
        console.error("Legacy profile migration failed:", e);
      }
    }
  },

  // Check if profile exists
  hasProfile(): boolean {
    if (!isBrowser()) return false;
    this.migrateLegacyIfNeeded();
    return Object.keys(this.getAllProfiles()).length > 0;
  },

  // Get active profile
  getProfile(): UserProfile | null {
    if (!isBrowser()) return null;
    this.migrateLegacyIfNeeded();
    const activeId = localStorage.getItem(LOCAL_STORAGE_KEY_ACTIVE);
    if (!activeId) return null;
    const profiles = this.getAllProfiles();
    const profile = profiles[activeId] || null;
    if (profile && APP_CONFIG.singleLevelMode) {
      profile.grade = APP_CONFIG.defaultGrade;
    }
    return profile;
  },

  // Get all profiles keyed by ID
  getAllProfiles(): Record<string, UserProfile> {
    if (!isBrowser()) return {};
    const data = localStorage.getItem(LOCAL_STORAGE_KEY_PROFILES);
    if (!data) return {};
    try {
      return JSON.parse(data) as Record<string, UserProfile>;
    } catch (e) {
      console.error("Error parsing profiles data:", e);
      return {};
    }
  },

  // Get all profiles as a sorted array
  getProfilesList(): UserProfile[] {
    const profiles = this.getAllProfiles();
    return Object.values(profiles).sort((a, b) => a.nickname.localeCompare(b.nickname));
  },

  // Set the active profile ID
  setActiveProfile(id: string): void {
    if (!isBrowser()) return;
    localStorage.setItem(LOCAL_STORAGE_KEY_ACTIVE, id);
    const profiles = this.getAllProfiles();
    const activeProfile = profiles[id];
    if (activeProfile) {
      const grade = APP_CONFIG.singleLevelMode ? APP_CONFIG.defaultGrade : activeProfile.grade;
      localStorage.setItem("preferredGrade", grade);
    }
    window.dispatchEvent(new Event("profileChanged"));
  },

  // Save/Update profile
  saveProfile(profile: UserProfile): void {
    if (!isBrowser()) return;
    if (APP_CONFIG.singleLevelMode) {
      profile.grade = APP_CONFIG.defaultGrade;
    }
    const profiles = this.getAllProfiles();
    profiles[profile.id] = profile;
    localStorage.setItem(LOCAL_STORAGE_KEY_PROFILES, JSON.stringify(profiles));
    // Dispatch a custom event so other components know the profile changed
    window.dispatchEvent(new Event("profileChanged"));
  },

  // Create new profile
  createProfile(nickname: string, avatar: string, grade: string): UserProfile {
    const uniqueId = "profile_" + Date.now() + "_" + Math.random().toString(36).substring(2, 7);
    const finalGrade = APP_CONFIG.singleLevelMode ? APP_CONFIG.defaultGrade : (grade || "grade3");
    const newProfile: UserProfile = {
      id: uniqueId,
      nickname: nickname.trim() || "Young Learner",
      avatar: avatar || "🐼",
      grade: finalGrade,
      learnedWords: [],
      quizScores: {},
      listeningScores: {}
    };
    this.saveProfile(newProfile);
    this.setActiveProfile(uniqueId);
    return newProfile;
  },

  // Delete profile by ID or active profile if ID is omitted
  deleteProfile(id?: string): void {
    if (!isBrowser()) return;
    const targetId = id || localStorage.getItem(LOCAL_STORAGE_KEY_ACTIVE);
    if (!targetId) return;

    const profiles = this.getAllProfiles();
    delete profiles[targetId];
    localStorage.setItem(LOCAL_STORAGE_KEY_PROFILES, JSON.stringify(profiles));
    
    const activeId = localStorage.getItem(LOCAL_STORAGE_KEY_ACTIVE);
    if (activeId === targetId) {
      const remainingIds = Object.keys(profiles);
      if (remainingIds.length > 0) {
        this.setActiveProfile(remainingIds[0]);
      } else {
        localStorage.removeItem(LOCAL_STORAGE_KEY_ACTIVE);
      }
    }
    window.dispatchEvent(new Event("profileChanged"));
  },

  // Mark word as learned
  markWordAsLearned(word: string): void {
    const profile = this.getProfile();
    if (!profile) return;

    if (!profile.learnedWords.includes(word)) {
      profile.learnedWords.push(word);
      this.saveProfile(profile);
    }
  },

  // Unmark word as learned
  unmarkWordAsLearned(word: string): void {
    const profile = this.getProfile();
    if (!profile) return;

    profile.learnedWords = profile.learnedWords.filter(w => w !== word);
    this.saveProfile(profile);
  },

  // Save Quiz High Score
  saveQuizScore(quizTitle: string, scorePercent: number): void {
    const profile = this.getProfile();
    if (!profile) return;

    const currentHighScore = profile.quizScores[quizTitle] || 0;
    if (scorePercent > currentHighScore) {
      profile.quizScores[quizTitle] = scorePercent;
      this.saveProfile(profile);
    }
  },

  // Save Listening High Score
  saveListeningScore(exerciseId: number, accuracyPercent: number): void {
    const profile = this.getProfile();
    if (!profile) return;

    const currentHighScore = profile.listeningScores[exerciseId] || 0;
    if (accuracyPercent > currentHighScore) {
      profile.listeningScores[exerciseId] = accuracyPercent;
      this.saveProfile(profile);
    }
  },

  // Calculate Stars
  calculateStars(profile: UserProfile): number {
    let stars = 0;

    // 1 star per learned word
    stars += profile.learnedWords.length;

    // Stars per quiz: 100% -> 3 stars, >=80% -> 2 stars, >=50% -> 1 star
    Object.values(profile.quizScores).forEach(score => {
      if (score === 100) stars += 3;
      else if (score >= 80) stars += 2;
      else if (score >= 50) stars += 1;
    });

    // Stars per listening exercise: 100% -> 3 stars, >=80% -> 2 stars, >=50% -> 1 star
    Object.values(profile.listeningScores).forEach(score => {
      if (score === 100) stars += 3;
      else if (score >= 80) stars += 2;
      else if (score >= 50) stars += 1;
    });

    return stars;
  },

  // Check which badges are unlocked
  getUnlockedBadges(profile: UserProfile): string[] {
    const unlocked: string[] = [];

    // vocab_novice: Learn 1 word
    if (profile.learnedWords.length >= 1) {
      unlocked.push("vocab_novice");
    }

    // vocab_master: Learn 8 words
    if (profile.learnedWords.length >= 8) {
      unlocked.push("vocab_master");
    }

    // quiz_champ: 100% on any quiz
    const hasPerfectQuiz = Object.values(profile.quizScores).some(score => score === 100);
    if (hasPerfectQuiz) {
      unlocked.push("quiz_champ");
    }

    // listening_pro: >=90% accuracy on listening task
    const hasListeningPro = Object.values(profile.listeningScores).some(score => score >= 90);
    if (hasListeningPro) {
      unlocked.push("listening_pro");
    }

    // star_collector: >=10 stars
    const totalStars = this.calculateStars(profile);
    if (totalStars >= 10) {
      unlocked.push("star_collector");
    }

    // super_scholar: at least 1 word, 1 quiz score, and 1 listening score
    const hasWord = profile.learnedWords.length >= 1;
    const hasQuiz = Object.keys(profile.quizScores).length >= 1;
    const hasListening = Object.keys(profile.listeningScores).length >= 1;
    if (hasWord && hasQuiz && hasListening) {
      unlocked.push("super_scholar");
    }

    return unlocked;
  },

  // Export active profile data to JSON string
  exportProfileData(): string {
    const profile = this.getProfile();
    return profile ? JSON.stringify(profile) : "";
  },

  // Import profile data from JSON string and add it to registry
  importProfileData(jsonString: string): boolean {
    try {
      const parsed = JSON.parse(jsonString) as any;
      // Basic validation
      if (typeof parsed.nickname === "string" && typeof parsed.avatar === "string" && typeof parsed.grade === "string") {
        const uniqueId = parsed.id || ("profile_" + Date.now() + "_" + Math.random().toString(36).substring(2, 7));
        const finalGrade = APP_CONFIG.singleLevelMode ? APP_CONFIG.defaultGrade : parsed.grade;
        const validatedProfile: UserProfile = {
          id: uniqueId,
          nickname: parsed.nickname,
          avatar: parsed.avatar,
          grade: finalGrade,
          learnedWords: Array.isArray(parsed.learnedWords) ? parsed.learnedWords : [],
          quizScores: parsed.quizScores && typeof parsed.quizScores === "object" ? parsed.quizScores : {},
          listeningScores: parsed.listeningScores && typeof parsed.listeningScores === "object" ? parsed.listeningScores : {}
        };
        this.saveProfile(validatedProfile);
        this.setActiveProfile(uniqueId);
        return true;
      }
    } catch (e) {
      console.error("Failed to import profile data:", e);
    }
    return false;
  }
};
