# Mixin methods for Submission and associated objects

class SubmissionMixin:
    def delete_dependencies(self, db):
        # repertoire and everything downstream
        for r in self.repertoire:
            r.delete_dependencies(db)
            db.session.delete(r)

        for n in self.notes_entries:
            db.session.delete(n)

        # acknowledgements
        for a in self.acknowledgements:
            db.session.delete(a)

        # journal entries
        for j in self.journal_entries:
            db.session.delete(j)

    def can_see(self, user):
        return(self.public or
            user.is_authenticated and
               #(user.has_role('Admin') or
                user.has_role(self.species) or \
                self.owner == user) or \
                user in self.delegates

    def can_edit(self, user):
        return(user.is_authenticated and
                #(user.has_role('Admin') or
                 (self.owner == user and self.submission_status == 'draft'))

    def can_see_private(self, user):
        return(user.is_authenticated and
                (self.owner == user or user.has_role(self.species) or user in self.delegates))