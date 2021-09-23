from comment import Comment

class Comments:
    def __init__(self, question):
        self.question = question
        self.comments = []
    
    # saves a comment given a question, points and its content
    def add_comment(self, question, points, content):
        self.comments.append(Comment(points, content))
    
    def get_comments(self):
        return self.comments
    
    def points_deducted(self):
        points_deducted = 0
        for comment in self.comments:
            points_deducted += comment.get_points_deducted
        return points_deducted