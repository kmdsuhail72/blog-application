from app.db.session import SessionLocal
from app.models.category import Category
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate
from app.services.post_service import PostService, make_slug

TOPICS = {
    "react": {
        "name": "React", "image": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?auto=format&fit=crop&w=1200&q=80",
        "titles": ["React Components That Stay Easy to Change", "How to Build Accessible React Forms", "Choosing Between Context and Props in React", "A Simple Strategy for React Loading States", "React Performance Checks That Actually Help"],
    },
    "python": {
        "name": "Python", "image": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?auto=format&fit=crop&w=1200&q=80",
        "titles": ["Writing Clear Python Functions", "Five Python Standard Library Tools to Know", "Practical Python Type Hints", "Organizing a Python Project for Growth", "Testing Python Code with Confidence"],
    },
    "devops": {
        "name": "DevOps", "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
        "titles": ["A Safer Path to Continuous Delivery", "Making CI Pipelines Faster and Clearer", "DevOps Metrics That Improve Delivery", "How to Plan a Useful Incident Review", "Keeping Application Configuration Manageable"],
    },
    "docker": {
        "name": "Docker", "image": "https://images.unsplash.com/photo-1605745341112-85968b19335b?auto=format&fit=crop&w=1200&q=80",
        "titles": ["Docker Images: A Practical Mental Model", "Writing Smaller Dockerfiles", "Using Docker Compose for Local Development", "Container Health Checks Without Guesswork", "Debugging Docker Networking Locally"],
    },
}


def content_for(topic: str, title: str) -> str:
    return f"""# {title}

Good {topic} work starts with small, understandable decisions. This guide focuses on a practical approach you can use in a real project.

## Start with the outcome

Define the behavior you need, keep the first implementation focused, and verify it with a short feedback loop.

## Keep the system maintainable

- Prefer clear names over clever shortcuts.
- Automate checks that prevent repeated mistakes.
- Document the decisions that future teammates need to understand.

The strongest improvements are the ones your team can sustain."""


db = SessionLocal()
try:
    user = db.query(User).filter(User.email == "welcome@example.com").first()
    if user is None:
        raise RuntimeError("The welcome author must exist before adding sample articles.")

    service = PostService()
    created = []
    for slug, topic in TOPICS.items():
        category = db.query(Category).filter(Category.slug == slug).first()
        if category is None:
            category = Category(name=topic["name"], slug=slug)
            db.add(category)
            db.commit()
            db.refresh(category)

        for title in topic["titles"]:
            if db.query(Post).filter(Post.slug == make_slug(title)).first() is not None:
                continue
            post = service.create_post(
                db,
                user.id,
                PostCreate(
                    title=title,
                    content=content_for(topic["name"], title),
                    category_id=category.id,
                    cover_image=topic["image"],
                    published=True,
                    tags=[topic["name"], "Guides"],
                ),
            )
            created.append(post.title)
    print({"created": len(created), "titles": created})
finally:
    db.close()
