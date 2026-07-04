from uuid import UUID
from datetime import date
from django.contrib.auth.models import User
from rh.infrastructure.models import EmployeModel
from administration.infrastructure.models import AgenceModel

class AgenceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("[Middleware] Appel du middleware")
        agence_id = None

        # Vérifier si l'utilisateur est authentifié
        print(f"[Middleware] request.user.is_authenticated = {request.user.is_authenticated}")
        if request.user.is_authenticated:
            try:
                print(f"[Middleware] ID de l'utilisateur : {request.user.id}")
                user = User.objects.get(id=request.user.id)
                email = user.email
                print(f"[Middleware] Utilisateur: {user.username}, Email: '{email}'")

                # FALLBACK pour fayagracia001
                if user.username == 'fayagracia001':
                    agence_id = UUID('145e663f-10e3-4deb-b990-104dce36c13c')
                    print(f"[Middleware] Fallback agence_id fixé à {agence_id} pour {user.username}")
                else:
                    if email:
                        try:
                            employe = EmployeModel.objects.get(email=email)
                            agence_id = employe.agence_id
                            print(f"[Middleware] agence_id trouvé: {agence_id}")
                        except EmployeModel.DoesNotExist:
                            print(f"[Middleware] Aucun employé pour l'email: {email}")
                            # Créer l'employé
                            agence = AgenceModel.objects.filter(actif=True).first()
                            if agence:
                                employe = EmployeModel.objects.create(
                                    matricule=f"EMP{user.id}",
                                    nom=user.first_name or user.username,
                                    prenom=user.last_name or "User",
                                    email=email,
                                    date_embauche=date.today(),
                                    taux_horaire=0,
                                    poste="Employé",
                                    agence_id=agence.id
                                )
                                agence_id = agence.id
                                print(f"[Middleware] Employé créé avec agence {agence.id}")
                            else:
                                print("[Middleware] Aucune agence active trouvée.")
                    else:
                        print("[Middleware] Email vide pour l'utilisateur.")
                        agence = AgenceModel.objects.filter(actif=True).first()
                        if agence:
                            agence_id = agence.id
                            print(f"[Middleware] Agence par défaut assignée (email vide)")
            except User.DoesNotExist:
                print("[Middleware] Utilisateur introuvable dans la base.")
            except Exception as e:
                print(f"[Middleware] Erreur inattendue : {e}")
                import traceback
                traceback.print_exc()

        request.agence_id = agence_id
        print(f"[Middleware] agence_id final: {agence_id}")
        return self.get_response(request)