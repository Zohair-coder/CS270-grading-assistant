class Comment:
    def __init__(self, points_deducted, comment):
        self.points_deducted = points_deducted
        self.comment = comment
    
    def get_points_deducted(self):
        return self.points_deducted
    
    def get_comment(self):
        return self.comment
