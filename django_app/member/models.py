from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class MyUserManager(UserManager):
    pass


class MyUser(AbstractUser):
    img_profile = models.ImageField(
        upload_to='photo/profile',
        blank=True
    )

    following_user = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Relationship',
        related_name='user_set_followers'
    )

    block_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='user_set_block'
    )

    def __str__(self):
        return self.get_full_name()

    def follow(self, user):
        instance, created = Relationship.objects.get_or_create(
            follower=self,
            following=user
        )
        return instance

    def unfollow(self, user):
        Relationship.objects.filter(
            follower=self,
            following=user
        ).delete()

    def friends(self):
        return self.following_user.all().filter(following_users=self)
        # follower_people = self.user_set_followers.all()
        # ans = [friend for friend in following_people if friend in follower_people]

    def block(self, user):
        self.block_users.add(user)

    def unblock(self, user):
        self.block_users.delete(user)

    def is_friends(self, user):
        if user in self.friends():
            return True
        return False


class Relationship(models.Model):
    following = models.ForeignKey(MyUser, related_name='user_following')
    follower = models.ForeignKey(MyUser, related_name='user_follower')
    created_date = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('following', 'follower')

    def __str__(self):
        return "{}(follower)가 {}를 following 했다.".format(self.follower, self.following)

