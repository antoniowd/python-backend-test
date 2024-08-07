"""Profile service module."""
from collections import deque
from typing import List, Optional
from .repositories import ProfileRepository
from app.models import Profile

class ProfileService:
    """Profile service."""
    def __init__(self, profile_repository: ProfileRepository):
        self.repo = profile_repository

    def get(self, id_: int) -> Profile | None:
        """Get a single profile by ID."""
        return self.repo.get(id_)

    def get_all(self) -> List[Profile]:
        """List all profiles."""
        return self.repo.get_all()

    def get_profile_friends(self, id_) -> List[Profile]:
        """List all profiles."""
        return self.repo.get_profile_friends(id_)

    def create(self, item: Profile) -> Profile:
        """Create a new profile."""
        return self.repo.create(item)

    def update(self, item: Profile) -> Profile | None:
        """Update a profile by ID."""
        return self.repo.update(item)

    def delete(self, id_: int) -> Profile | None:
        """Delete a profile by ID."""
        return self.repo.delete(id_)

    def get_shorter_connection(self, profile_id: int, friend_id: int) -> Optional[List[int]]:
        """Get the shortest connection between two profiles."""
        if profile_id == friend_id:
            return [profile_id]

        queue = deque([(profile_id, [])])
        visited = set()

        while queue:
            current_id, connection = queue.popleft()
            if current_id in visited:
                continue
            visited.add(current_id)

            friends = self.repo.get_profile_friends(current_id)
            for friend in friends:
                if friend.id == friend_id:
                    if len(connection) == 0:
                        return [friend_id]
                    return connection

                queue.append((friend.id, connection + [friend.id]))

        return None
