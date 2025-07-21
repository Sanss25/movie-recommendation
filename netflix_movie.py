import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import math

class NetflixMovieRecommender:
    def __init__(self):
        self.movies = self._initialize_movie_database()
        self.user_profiles = {}
        self.viewing_history = {}
        self.ratings = {}
        self.watchlist = {}
        self.trending_movies = []
        self.new_releases = []
        self._generate_trending_and_new()
    
    def _initialize_movie_database(self) -> List[Dict]:
        """Initialize a comprehensive movie database with Netflix-style categories"""
        return [
            # Action Movies
            {"id": 1, "title": "Extraction 2", "genre": ["Action", "Thriller"], "year": 2023, "rating": 7.8, "duration": 122, "category": "Netflix Original", "tags": ["military", "rescue", "intense"]},
            {"id": 2, "title": "The Gray Man", "genre": ["Action", "Thriller"], "year": 2022, "rating": 6.5, "duration": 129, "category": "Netflix Original", "tags": ["spy", "chase", "assassin"]},
            {"id": 3, "title": "Red Notice", "genre": ["Action", "Comedy"], "year": 2021, "rating": 6.3, "duration": 118, "category": "Netflix Original", "tags": ["heist", "art", "comedy"]},
            
            # Sci-Fi
            {"id": 4, "title": "The Adam Project", "genre": ["Sci-Fi", "Action"], "year": 2022, "rating": 6.7, "duration": 106, "category": "Netflix Original", "tags": ["time travel", "family", "adventure"]},
            {"id": 5, "title": "Stowaway", "genre": ["Sci-Fi", "Thriller"], "year": 2021, "rating": 5.7, "duration": 116, "category": "Netflix Original", "tags": ["space", "survival", "drama"]},
            {"id": 6, "title": "I Am Mother", "genre": ["Sci-Fi", "Thriller"], "year": 2019, "rating": 6.7, "duration": 113, "category": "Netflix Original", "tags": ["AI", "dystopian", "mystery"]},
            
            # Horror/Thriller
            {"id": 7, "title": "His House", "genre": ["Horror", "Drama"], "year": 2020, "rating": 6.5, "duration": 93, "category": "Netflix Original", "tags": ["supernatural", "refugee", "psychological"]},
            {"id": 8, "title": "Bird Box", "genre": ["Horror", "Thriller"], "year": 2018, "rating": 6.6, "duration": 124, "category": "Netflix Original", "tags": ["post-apocalyptic", "survival", "mystery"]},
            {"id": 9, "title": "The Platform", "genre": ["Horror", "Sci-Fi"], "year": 2019, "rating": 7.0, "duration": 94, "category": "Netflix Original", "tags": ["dystopian", "social commentary", "psychological"]},
            
            # Romance/Drama
            {"id": 10, "title": "To All the Boys I've Loved Before", "genre": ["Romance", "Comedy"], "year": 2018, "rating": 7.0, "duration": 99, "category": "Netflix Original", "tags": ["teen", "love letters", "high school"]},
            {"id": 11, "title": "The Kissing Booth", "genre": ["Romance", "Comedy"], "year": 2018, "rating": 6.0, "duration": 105, "category": "Netflix Original", "tags": ["teen", "friendship", "romance"]},
            {"id": 12, "title": "Marriage Story", "genre": ["Drama", "Romance"], "year": 2019, "rating": 7.9, "duration": 137, "category": "Netflix Original", "tags": ["divorce", "family", "emotional"]},
            
            # International Content
            {"id": 13, "title": "Roma", "genre": ["Drama"], "year": 2018, "rating": 7.7, "duration": 135, "category": "Netflix Original", "tags": ["black and white", "mexico", "family"]},
            {"id": 14, "title": "Okja", "genre": ["Adventure", "Drama"], "year": 2017, "rating": 7.3, "duration": 120, "category": "Netflix Original", "tags": ["animal friendship", "corporate", "korean"]},
            {"id": 15, "title": "The Ballad of Buster Scruggs", "genre": ["Western", "Comedy"], "year": 2018, "rating": 7.2, "duration": 133, "category": "Netflix Original", "tags": ["anthology", "dark comedy", "western"]},
            
            # Comedy
            {"id": 16, "title": "Murder Mystery", "genre": ["Comedy", "Mystery"], "year": 2019, "rating": 6.0, "duration": 97, "category": "Netflix Original", "tags": ["vacation", "whodunit", "comedy"]},
            {"id": 17, "title": "The Do-Over", "genre": ["Comedy", "Action"], "year": 2016, "rating": 5.7, "duration": 108, "category": "Netflix Original", "tags": ["identity", "friendship", "action comedy"]},
            {"id": 18, "title": "Wine Country", "genre": ["Comedy"], "year": 2019, "rating": 5.5, "duration": 103, "category": "Netflix Original", "tags": ["friendship", "wine", "vacation"]},
            
            # Documentaries
            {"id": 19, "title": "My Octopus Teacher", "genre": ["Documentary"], "year": 2020, "rating": 8.1, "duration": 85, "category": "Netflix Original", "tags": ["nature", "ocean", "inspiring"]},
            {"id": 20, "title": "The Social Dilemma", "genre": ["Documentary"], "year": 2020, "rating": 7.6, "duration": 94, "category": "Netflix Original", "tags": ["technology", "social media", "society"]},
            
            # Licensed Content (Popular Movies)
            {"id": 21, "title": "The Shawshank Redemption", "genre": ["Drama"], "year": 1994, "rating": 9.3, "duration": 142, "category": "Classic", "tags": ["prison", "friendship", "hope"]},
            {"id": 22, "title": "Inception", "genre": ["Sci-Fi", "Thriller"], "year": 2010, "rating": 8.8, "duration": 148, "category": "Blockbuster", "tags": ["dreams", "heist", "mind-bending"]},
            {"id": 23, "title": "The Dark Knight", "genre": ["Action", "Crime"], "year": 2008, "rating": 9.0, "duration": 152, "category": "Superhero", "tags": ["batman", "joker", "crime"]},
            {"id": 24, "title": "Pulp Fiction", "genre": ["Crime", "Drama"], "year": 1994, "rating": 8.9, "duration": 154, "category": "Classic", "tags": ["nonlinear", "crime", "dialogue"]},
            {"id": 25, "title": "Forrest Gump", "genre": ["Drama", "Romance"], "year": 1994, "rating": 8.8, "duration": 142, "category": "Classic", "tags": ["life story", "historical", "inspiring"]},
        ]
    
    def create_user_profile(self, username: str, preferences: Dict) -> None:
        """Create a new user profile with preferences"""
        self.user_profiles[username] = {
            "favorite_genres": preferences.get("favorite_genres", []),
            "disliked_genres": preferences.get("disliked_genres", []),
            "preferred_rating_range": preferences.get("preferred_rating_range", [6.0, 10.0]),
            "preferred_duration_range": preferences.get("preferred_duration_range", [60, 180]),
            "language_preference": preferences.get("language_preference", "English"),
            "maturity_rating": preferences.get("maturity_rating", "All"),
            "created_date": datetime.now()
        }
        self.viewing_history[username] = []
        self.ratings[username] = {}
        self.watchlist[username] = []
        print(f"Profile created for {username}")
    
    def add_to_watchlist(self, username: str, movie_id: int) -> None:
        """Add a movie to user's watchlist"""
        if username not in self.user_profiles:
            print("User profile not found")
            return
        
        if movie_id not in [movie["id"] for movie in self.movies]:
            print("Movie not found")
            return
        
        if movie_id not in self.watchlist[username]:
            self.watchlist[username].append(movie_id)
            movie_title = next(m["title"] for m in self.movies if m["id"] == movie_id)
            print(f"Added '{movie_title}' to watchlist")
        else:
            print("Movie already in watchlist")
    
    def remove_from_watchlist(self, username: str, movie_id: int) -> None:
        """Remove a movie from user's watchlist"""
        if username in self.watchlist and movie_id in self.watchlist[username]:
            self.watchlist[username].remove(movie_id)
            movie_title = next(m["title"] for m in self.movies if m["id"] == movie_id)
            print(f"Removed '{movie_title}' from watchlist")
    
    def watch_movie(self, username: str, movie_id: int) -> None:
        """Record that a user watched a movie"""
        if username not in self.user_profiles:
            print("User profile not found")
            return
        
        movie = next((m for m in self.movies if m["id"] == movie_id), None)
        if not movie:
            print("Movie not found")
            return
        
        watch_record = {
            "movie_id": movie_id,
            "watched_date": datetime.now(),
            "completion_percentage": random.randint(70, 100)  # Simulate completion
        }
        
        self.viewing_history[username].append(watch_record)
        
        # Remove from watchlist if present
        if movie_id in self.watchlist.get(username, []):
            self.watchlist[username].remove(movie_id)
        
        print(f"Recorded viewing of '{movie['title']}'")
    
    def rate_movie(self, username: str, movie_id: int, rating: float) -> None:
        """Allow user to rate a movie (1-10 scale)"""
        if username not in self.user_profiles:
            print("User profile not found")
            return
        
        if not 1 <= rating <= 10:
            print("Rating must be between 1 and 10")
            return
        
        self.ratings[username][movie_id] = rating
        movie_title = next(m["title"] for m in self.movies if m["id"] == movie_id)
        print(f"Rated '{movie_title}': {rating}/10")
    
    def _generate_trending_and_new(self) -> None:
        """Generate trending movies and new releases"""
        # Simulate trending based on recent Netflix originals and high ratings
        netflix_originals = [m for m in self.movies if m["category"] == "Netflix Original"]
        self.trending_movies = sorted(netflix_originals, key=lambda x: x["rating"], reverse=True)[:8]
        
        # New releases (movies from 2022-2023)
        self.new_releases = [m for m in self.movies if m["year"] >= 2022]
    
    def get_trending_movies(self) -> List[Dict]:
        """Get currently trending movies"""
        return self.trending_movies
    
    def get_new_releases(self) -> List[Dict]:
        """Get new releases"""
        return self.new_releases
    
    def search_movies(self, query: str, filters: Optional[Dict] = None) -> List[Dict]:
        """Search for movies with optional filters"""
        results = []
        query_lower = query.lower()
        
        for movie in self.movies:
            # Search in title, genre, and tags
            if (query_lower in movie["title"].lower() or 
                any(query_lower in genre.lower() for genre in movie["genre"]) or
                any(query_lower in tag.lower() for tag in movie.get("tags", []))):
                results.append(movie)
        
        # Apply filters if provided
        if filters:
            if "genre" in filters:
                results = [m for m in results if any(g in m["genre"] for g in filters["genre"])]
            if "year_range" in filters:
                min_year, max_year = filters["year_range"]
                results = [m for m in results if min_year <= m["year"] <= max_year]
            if "rating_min" in filters:
                results = [m for m in results if m["rating"] >= filters["rating_min"]]
            if "category" in filters:
                results = [m for m in results if m["category"] == filters["category"]]
        
        return results[:20]  # Limit results
    
    def get_recommendations(self, username: str, recommendation_type: str = "for_you") -> List[Dict]:
        """Get personalized recommendations"""
        if username not in self.user_profiles:
            print("User profile not found")
            return []
        
        user_profile = self.user_profiles[username]
        user_history = self.viewing_history.get(username, [])
        user_ratings = self.ratings.get(username, {})
        
        if recommendation_type == "for_you":
            return self._get_personalized_recommendations(username)
        elif recommendation_type == "because_you_watched":
            return self._get_because_you_watched_recommendations(username)
        elif recommendation_type == "top_picks":
            return self._get_top_picks(username)
        elif recommendation_type == "trending_now":
            return self.get_trending_movies()
        elif recommendation_type == "new_releases":
            return self.get_new_releases()
        else:
            return self._get_personalized_recommendations(username)
    
    def _get_personalized_recommendations(self, username: str) -> List[Dict]:
        """Generate personalized recommendations based on user profile and history"""
        user_profile = self.user_profiles[username]
        watched_movie_ids = [record["movie_id"] for record in self.viewing_history.get(username, [])]
        
        candidates = []
        for movie in self.movies:
            if movie["id"] in watched_movie_ids:
                continue
            
            score = 0
            
            # Genre preference scoring
            for genre in movie["genre"]:
                if genre in user_profile["favorite_genres"]:
                    score += 3
                elif genre in user_profile.get("disliked_genres", []):
                    score -= 2
            
            # Rating preference
            rating_min, rating_max = user_profile["preferred_rating_range"]
            if rating_min <= movie["rating"] <= rating_max:
                score += 2
            
            # Duration preference
            duration_min, duration_max = user_profile["preferred_duration_range"]
            if duration_min <= movie["duration"] <= duration_max:
                score += 1
            
            # Boost Netflix Originals slightly
            if movie["category"] == "Netflix Original":
                score += 0.5
            
            # Boost newer content
            if movie["year"] >= 2020:
                score += 1
            
            candidates.append((movie, score))
        
        # Sort by score and return top recommendations
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [movie for movie, score in candidates[:10]]
    
    def _get_because_you_watched_recommendations(self, username: str) -> List[Dict]:
        """Generate recommendations based on recently watched movies"""
        user_history = self.viewing_history.get(username, [])
        if not user_history:
            return self._get_personalized_recommendations(username)
        
        # Get the most recently watched movie
        recent_watch = user_history[-1]
        recent_movie = next(m for m in self.movies if m["id"] == recent_watch["movie_id"])
        
        recommendations = []
        watched_ids = [record["movie_id"] for record in user_history]
        
        for movie in self.movies:
            if movie["id"] in watched_ids:
                continue
            
            similarity_score = 0
            
            # Same genre
            common_genres = set(movie["genre"]) & set(recent_movie["genre"])
            similarity_score += len(common_genres) * 2
            
            # Similar tags
            common_tags = set(movie.get("tags", [])) & set(recent_movie.get("tags", []))
            similarity_score += len(common_tags)
            
            # Similar category
            if movie["category"] == recent_movie["category"]:
                similarity_score += 1
            
            # Similar year (within 5 years)
            if abs(movie["year"] - recent_movie["year"]) <= 5:
                similarity_score += 0.5
            
            if similarity_score > 0:
                recommendations.append((movie, similarity_score))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [movie for movie, score in recommendations[:8]]
    
    def _get_top_picks(self, username: str) -> List[Dict]:
        """Get top picks for user based on high ratings and user preferences"""
        user_profile = self.user_profiles[username]
        watched_ids = [record["movie_id"] for record in self.viewing_history.get(username, [])]
        
        candidates = []
        for movie in self.movies:
            if movie["id"] in watched_ids:
                continue
            
            # High rating movies (8.0+)
            if movie["rating"] >= 8.0:
                score = movie["rating"]
                
                # Boost if matches user's favorite genres
                for genre in movie["genre"]:
                    if genre in user_profile["favorite_genres"]:
                        score += 1
                
                candidates.append((movie, score))
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [movie for movie, score in candidates[:8]]
    
    def get_user_stats(self, username: str) -> Dict:
        """Get user viewing statistics"""
        if username not in self.user_profiles:
            return {}
        
        history = self.viewing_history.get(username, [])
        ratings_data = self.ratings.get(username, {})
        
        if not history:
            return {"message": "No viewing history found"}
        
        # Calculate stats
        total_movies = len(history)
        total_minutes = sum(next(m["duration"] for m in self.movies if m["id"] == record["movie_id"]) 
                          for record in history)
        
        # Favorite genres
        genre_count = {}
        for record in history:
            movie = next(m for m in self.movies if m["id"] == record["movie_id"])
            for genre in movie["genre"]:
                genre_count[genre] = genre_count.get(genre, 0) + 1
        
        favorite_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Average rating given
        avg_rating = sum(ratings_data.values()) / len(ratings_data) if ratings_data else 0
        
        return {
            "total_movies_watched": total_movies,
            "total_hours_watched": round(total_minutes / 60, 1),
            "favorite_genres": [genre for genre, count in favorite_genres],
            "average_rating_given": round(avg_rating, 1),
            "watchlist_count": len(self.watchlist.get(username, [])),
            "movies_rated": len(ratings_data)
        }
    
    def display_movie_info(self, movie: Dict) -> None:
        """Display formatted movie information"""
        print(f"\n🎬 {movie['title']} ({movie['year']})")
        print(f"⭐ Rating: {movie['rating']}/10")
        print(f"🎭 Genre: {', '.join(movie['genre'])}")
        print(f"⏱️  Duration: {movie['duration']} minutes")
        print(f"📺 Category: {movie['category']}")
        if movie.get('tags'):
            print(f"🏷️  Tags: {', '.join(movie['tags'])}")
        print("-" * 50)

def main():
    """Main function to demonstrate the Netflix movie recommender"""
    recommender = NetflixMovieRecommender()
    
    print("🎬 Welcome to Netflix Movie Recommender! 🎬\n")
    
    # Create a sample user
    sample_preferences = {
        "favorite_genres": ["Action", "Sci-Fi", "Thriller"],
        "disliked_genres": ["Horror"],
        "preferred_rating_range": [7.0, 10.0],
        "preferred_duration_range": [90, 150],
        "maturity_rating": "All"
    }
    
    username = "movie_lover"
    recommender.create_user_profile(username, sample_preferences)
    
    # Simulate some viewing activity
    recommender.watch_movie(username, 1)  # Extraction 2
    recommender.rate_movie(username, 1, 8.5)
    recommender.watch_movie(username, 4)  # The Adam Project
    recommender.rate_movie(username, 4, 7.0)
    recommender.add_to_watchlist(username, 22)  # Inception
    
    while True:
        print("\n" + "="*60)
        print("NETFLIX MOVIE RECOMMENDER MENU")
        print("="*60)
        print("1. Get Personalized Recommendations")
        print("2. Search Movies")
        print("3. View Trending Movies")
        print("4. View New Releases")
        print("5. Add to Watchlist")
        print("6. Rate a Movie")
        print("7. View My Stats")
        print("8. View Watchlist")
        print("9. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == "1":
            print("\nSelect recommendation type:")
            print("1. For You")
            print("2. Because You Watched")
            print("3. Top Picks")
            print("4. Trending Now")
            
            rec_choice = input("Enter choice (1-4): ").strip()
            rec_types = {"1": "for_you", "2": "because_you_watched", 
                        "3": "top_picks", "4": "trending_now"}
            
            if rec_choice in rec_types:
                recommendations = recommender.get_recommendations(username, rec_types[rec_choice])
                print(f"\n🎯 Recommendations ({rec_types[rec_choice].replace('_', ' ').title()}):")
                for i, movie in enumerate(recommendations[:5], 1):
                    print(f"{i}. {movie['title']} ({movie['year']}) - {movie['rating']}/10")
        
        elif choice == "2":
            query = input("Enter search query: ").strip()
            if query:
                results = recommender.search_movies(query)
                if results:
                    print(f"\n🔍 Search Results for '{query}':")
                    for i, movie in enumerate(results[:10], 1):
                        print(f"{i}. {movie['title']} ({movie['year']}) - {', '.join(movie['genre'])}")
                else:
                    print("No movies found matching your search.")
        
        elif choice == "3":
            trending = recommender.get_trending_movies()
            print("\n🔥 Trending Movies:")
            for i, movie in enumerate(trending, 1):
                print(f"{i}. {movie['title']} ({movie['year']}) - {movie['rating']}/10")
        
        elif choice == "4":
            new_releases = recommender.get_new_releases()
            print("\n🆕 New Releases:")
            for i, movie in enumerate(new_releases, 1):
                print(f"{i}. {movie['title']} ({movie['year']}) - {movie['rating']}/10")
        
        elif choice == "5":
            movie_id = input("Enter movie ID to add to watchlist: ").strip()
            try:
                recommender.add_to_watchlist(username, int(movie_id))
            except ValueError:
                print("Please enter a valid movie ID number.")
        
        elif choice == "6":
            try:
                movie_id = int(input("Enter movie ID to rate: ").strip())
                rating = float(input("Enter rating (1-10): ").strip())
                recommender.rate_movie(username, movie_id, rating)
            except ValueError:
                print("Please enter valid numbers.")
        
        elif choice == "7":
            stats = recommender.get_user_stats(username)
            print("\n📊 Your Netflix Stats:")
            for key, value in stats.items():
                if key != "message":
                    print(f"{key.replace('_', ' ').title()}: {value}")
        
        elif choice == "8":
            watchlist_ids = recommender.watchlist.get(username, [])
            if watchlist_ids:
                print("\n📋 Your Watchlist:")
                for movie_id in watchlist_ids:
                    movie = next(m for m in recommender.movies if m["id"] == movie_id)
                    print(f"• {movie['title']} ({movie['year']})")
            else:
                print("\n📋 Your watchlist is empty.")
        
        elif choice == "9":
            print("Thanks for using Netflix Movie Recommender! 🎬")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()