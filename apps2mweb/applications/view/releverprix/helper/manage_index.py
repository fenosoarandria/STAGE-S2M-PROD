from django.db import connections

#Vitesse de Recherche : Les index accélèrent les opérations de recherche, de tri, et de filtrage dans les requêtes SQL.

def manage_indexes_releve(action):
    """ Crée ou supprime des index en fonction de l'action spécifiée. """
    with connections['default'].cursor() as cursor:
        if action == 'create':
            # Vérifier si les index existent déjà
            cursor.execute("""
                SHOW INDEX FROM rel_releve WHERE Key_name = 'idx_ref_rel';
            """)
            if not cursor.fetchone():
                cursor.execute("""
                    CREATE INDEX idx_ref_rel ON rel_releve (ref_rel);
                """)
            
            cursor.execute("""
                SHOW INDEX FROM rel_art_concur WHERE Key_name = 'idx_ref_ac';
            """)
            if not cursor.fetchone():
                cursor.execute("""
                    CREATE INDEX idx_ref_ac ON rel_art_concur (ref_ac);
                """)
            
            cursor.execute("""
                SHOW INDEX FROM rel_art_concur WHERE Key_name = 'idx_enseigne_ac';
            """)
            if not cursor.fetchone():
                cursor.execute("""
                    CREATE INDEX idx_enseigne_ac ON rel_art_concur (enseigne_ac);
                """)
                
        elif action == 'drop':
            # Supprimer les index s'ils existent
            cursor.execute("""
                SHOW INDEX FROM rel_releve WHERE Key_name = 'idx_ref_rel';
            """)
            if cursor.fetchone():
                cursor.execute("""
                    DROP INDEX idx_ref_rel ON rel_releve;
                """)
            
            cursor.execute("""
                SHOW INDEX FROM rel_art_concur WHERE Key_name = 'idx_ref_ac';
            """)
            if cursor.fetchone():
                cursor.execute("""
                    DROP INDEX idx_ref_ac ON rel_art_concur;
                """)
            
            cursor.execute("""
                SHOW INDEX FROM rel_art_concur WHERE Key_name = 'idx_enseigne_ac';
            """)
            if cursor.fetchone():
                cursor.execute("""
                    DROP INDEX idx_enseigne_ac ON rel_art_concur;
                """)


def manage_indexes_rattachement(action):
    """ Crée ou supprime des index en fonction de l'action spécifiée. """
    with connections['default'].cursor() as cursor:
        if action == 'create':
            cursor.execute("""
                SHOW INDEX FROM rel_art_concur WHERE Key_name = 'idx_ref_ac';
            """)
            if not cursor.fetchone():
                cursor.execute("""
                    CREATE INDEX idx_ref_ac ON rel_art_concur (ref_ac);
                """)

            cursor.execute("""
                SHOW INDEX FROM rel_art_concur WHERE Key_name = 'idx_enseigne_ac';
            """)
            if not cursor.fetchone():
                cursor.execute("""
                    CREATE INDEX idx_enseigne_ac ON rel_art_concur (enseigne_ac);
                """)
                
        elif action == 'drop':
            cursor.execute("""
                SHOW INDEX FROM rel_art_concur WHERE Key_name = 'idx_ref_ac';
            """)
            if cursor.fetchone():
                cursor.execute("""
                    DROP INDEX idx_ref_ac ON rel_art_concur;
                """)

            cursor.execute("""
                SHOW INDEX FROM rel_art_concur WHERE Key_name = 'idx_enseigne_ac';
            """)
            if cursor.fetchone():
                cursor.execute("""
                    DROP INDEX idx_enseigne_ac ON rel_art_concur;
                """)

from django.db import connections

def manage_releve_existing(action):
    """ Crée ou supprime des index en fonction de l'action spécifiée. """
    with connections['default'].cursor() as cursor:
        if action == 'create':
            # Créer les index nécessaires pour optimiser la requête SQL
            # Vérifier si les index existent déjà
            indexes = [
                ('idx_ref_rel', 'rel_releve', 'ref_rel'),
                ('idx_gencod_rel', 'rel_releve', 'gencod_rel'),
                ('idx_libelle_art_rel', 'rel_releve', 'libelle_art_rel'),
                ('idx_enseigne_ens', 'rel_enseigne', 'enseigne_ens'),
                ('idx_id_releve', 'rel_index_releve', 'id_releve'),
                ('idx_enseigne_releve', 'rel_index_releve', 'enseigne_releve')
            ]
            for index_name, table, column in indexes:
                cursor.execute(f"""
                    SHOW INDEX FROM {table} WHERE Key_name = '{index_name}';
                """)
                if not cursor.fetchone():
                    cursor.execute(f"""
                        CREATE INDEX {index_name} ON {table} ({column});
                    """)

        elif action == 'drop':
            # Supprimer les index s'ils existent
            indexes = [
                ('idx_ref_rel', 'rel_releve'),
                ('idx_gencod_rel', 'rel_releve'),
                ('idx_libelle_art_rel', 'rel_releve'),
                ('idx_enseigne_ens', 'rel_enseigne'),
                ('idx_id_releve', 'rel_index_releve'),
                ('idx_enseigne_releve', 'rel_index_releve')
            ]
            for index_name, table in indexes:
                cursor.execute(f"""
                    SHOW INDEX FROM {table} WHERE Key_name = '{index_name}';
                """)
                if cursor.fetchone():
                    cursor.execute(f"""
                        DROP INDEX {index_name} ON {table};
                    """)
