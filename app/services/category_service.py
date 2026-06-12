from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate
from app.schemas.category import CategoryUpdate


class CategoryService:

    @staticmethod
    def create(
        db: Session,
        request: CategoryCreate
    ):
        existing_category = (
            CategoryRepository.get_by_name(
                db,
                request.name
            )
        )

        if existing_category:
            raise ValueError(
                "Category already exists"
            )

        category = Category(
            name=request.name,
            description=request.description
        )

        return CategoryRepository.create(
            db,
            category
        )

    @staticmethod
    def get_all(
        db: Session
    ):
        return CategoryRepository.get_all(db)

    @staticmethod
    def get_by_id(
        db: Session,
        category_id: str
    ):
        category = (
            CategoryRepository.get_by_id(
                db,
                category_id
            )
        )

        if not category:
            raise ValueError(
                "Category not found"
            )

        return category

    @staticmethod
    def update(
        db: Session,
        category_id: str,
        request: CategoryUpdate
    ):
        category = (
            CategoryRepository.get_by_id(
                db,
                category_id
            )
        )

        if not category:
            raise ValueError(
                "Category not found"
            )

        category.name = request.name
        category.description = request.description
        category.is_active = request.is_active

        db.commit()
        db.refresh(category)

        return category

    @staticmethod
    def delete(
        db: Session,
        category_id: str
    ):
        category = (
            CategoryRepository.get_by_id(
                db,
                category_id
            )
        )

        if not category:
            raise ValueError(
                "Category not found"
            )

        CategoryRepository.delete(
            db,
            category
        )