from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

# Models

class Movie(BaseModel):
    title: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    duration: int = Field(..., gt=30)
    rating: float = Field(..., ge=0, le=10)

class BookingRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    movie_id: int = Field(..., gt=0)
    seats: int = Field(..., gt=0, le=10)

class PaymentRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    payment_method: str = Field(...)

#Data

movies = [
    {"id": 1, "title": "Avengers", "genre": "Action", "duration": 180, "rating": 8.5},
    {"id": 2, "title": "Inception", "genre": "Sci-Fi", "duration": 150, "rating": 9.0},
    {"id": 4, "title": "Dhurandhar", "genre": "Action", "duration": 200, "rating": 8.2},
    {"id": 5, "title": "Taare Zameen Par", "genre": "Family/Musical", "duration": 195, "rating": 8.3},
    {"id": 6, "title": "3 Idiots", "genre": "Comedy/Romance", "duration": 215, "rating": 8.4},
]

bookings = []
booking_counter = 1
cart = []

#Helper Functions

def find_movie(movie_id: int):
    for m in movies:
        if m["id"] == movie_id:
            return m
    return None

def calculate_total(seats: int):
    return seats * 200  

def filter_movies_logic(genre=None, min_rating=None):
    result = movies
    if genre is not None:
        result = [m for m in result if m["genre"] == genre]
    if min_rating is not None:
        result = [m for m in result if m["rating"] >= min_rating]
    return result


@app.get("/")
def home():
    return {"message": "Welcome to Movie Ticket Booking API"}

@app.get("/movies")
def get_all_movies():
    return {"movies": movies, "total": len(movies)}

@app.get("/movies/count")
def get_movie_count():
    return {"total_movies": len(movies)}    


@app.get("/movies/filter")
def filter_movies(
    genre: str = Query(None),
    min_rating: float = Query(None)
):
    result = filter_movies_logic(genre, min_rating)
    return {"filtered_movies": result, "count": len(result)}


@app.get("/movies/compare")
def compare_movies(movie1: int = Query(...), movie2: int = Query(...)):
    m1 = find_movie(movie1)
    m2 = find_movie(movie2)

    if not m1 or not m2:
        return {"error": "One or both movies not found"}

    better = m1 if m1["rating"] > m2["rating"] else m2

    return {
        "movie_1": m1,
        "movie_2": m2,
        "better_movie": better["title"]
    }


@app.get("/movies/top-rated")
def top_rated_movies():
    top = [m for m in movies if m["rating"] >= 8]
    return {"top_movies": top}


#Search

@app.get("/movies/search")
def search_movies(keyword: str = Query(...)):
    results = [m for m in movies if keyword.lower() in m["title"].lower()]
    return {"results": results, "count": len(results)}

#Sort 

@app.get("/movies/sort")
def sort_movies(sort_by: str = Query("rating"), order: str = Query("desc")):
    reverse = order == "desc"
    sorted_movies = sorted(movies, key=lambda x: x[sort_by], reverse=reverse)
    return {"movies": sorted_movies}

#Pagination 

@app.get("/movies/page")
def paginate_movies(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    end = start + limit
    return {
        "page": page,
        "movies": movies[start:end]
    }

#CRUD

@app.post("/movies")
def add_movie(movie: Movie, response: Response):
    new_id = max(m["id"] for m in movies) + 1
    new_movie = {"id": new_id, **movie.dict()}
    movies.append(new_movie)
    response.status_code = status.HTTP_201_CREATED
    return {"message": "Movie added", "movie": new_movie}

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, rating: float = Query(None)):
    movie = find_movie(movie_id)
    if not movie:
        return {"error": "Movie not found"}
    if rating:
        movie["rating"] = rating
    return {"message": "Updated", "movie": movie}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        return {"error": "Movie not found"}
    movies.remove(movie)
    return {"message": "Movie deleted"}

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        return {"error": "Movie not found"}
    return {"movie": movie}


# Add to cart
@app.post("/cart/add")
def add_to_cart(movie_id: int = Query(...), seats: int = Query(1)):
    movie = find_movie(movie_id)
    if not movie:
        return {"error": "Movie not found"}

    cart_item = {
        "movie_id": movie_id,
        "movie_name": movie["title"],
        "seats": seats,
        "total": calculate_total(seats)
    }
    cart.append(cart_item)
    return {"message": "Added to cart", "item": cart_item}

#View cart
@app.get("/cart")
def view_cart():
    return {
        "items": cart,
        "total_amount": sum(item["total"] for item in cart)
    }

#Payment + Booking
@app.post("/cart/checkout")
def checkout(payment: PaymentRequest, response: Response):
    global booking_counter

    if not cart:
        return {"error": "Cart is empty"}

    booked = []

    for item in cart:
        booking = {
            "booking_id": booking_counter,
            "customer": payment.customer_name,
            "movie": item["movie_name"],
            "seats": item["seats"],
            "total": item["total"],
            "status": "confirmed"
        }
        bookings.append(booking)
        booked.append(booking)
        booking_counter += 1

    cart.clear()
    response.status_code = status.HTTP_201_CREATED

    return {"message": "Booking confirmed", "bookings": booked}


@app.delete("/cart/{movie_id}")
def remove_from_cart(movie_id: int):
    for item in cart:
        if item["movie_id"] == movie_id:
            cart.remove(item)
            return {"message": "Removed from cart"}
    return {"error": "Movie not in cart"}    

#View Bookings

@app.get("/bookings")
def get_bookings():
    return {"bookings": bookings}
