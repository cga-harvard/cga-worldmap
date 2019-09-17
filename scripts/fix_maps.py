import psycopg2

cs = 'host=*** dbname=*** user=*** password=***'

base_maps = {
    'OpenStreetMap': [1, True, '{"selected": false, "title": "OpenStreetMap", "args": ["OpenStreetMap"], "type": "OpenLayers.Layer.OSM"}', '{"id": "1", "ptype": "gx_olsource"}'],
    'No background': [0, False, '{"selected": false, "title": "No background", "args": ["No background"], "type": "OpenLayers.Layer"}', '{"id": "1", "ptype": "gx_olsource"}'],
    'watercolor': [2, False, '{"title": "Stamen Watercolor", "selected": false}', '{"id": "3", "ptype": "gxp_stamensource"}'],
    'toner': [3, False, '{"title": "Stamen Toner", "selected": false}', '{"id": "3", "ptype": "gxp_stamensource"}'],
}

def fix_map(id):
    print('Fixing maps %s...' % id)
    conn = psycopg2.connect(cs)
    cur = conn.cursor()

    # 1. delete baselayers for the map
    cur.execute("DELETE FROM maps_maplayer WHERE map_id = %s AND \"group\" = 'background'" % id)

    # 2. add the baselayers again
    for k, v in base_maps.items():
        sql = """
            INSERT INTO maps_maplayer
            (map_id, stack_order, name, opacity, transparent, fixed, "group", visibility,
            layer_params, source_params)
            VALUES
            (%s, %s, '%s', 1, False, True, 'background', %s, '%s', '%s')
        """ % (id, v[0], k, v[1], v[2], v[3])
        cur.execute(sql)

    conn.commit()


def get_map_ids():
    conn = psycopg2.connect(cs)
    cur = conn.cursor()
    cur.execute('SELECT * FROM id FROM maps_map;')
    return [r[0] for r in cur.fetchall()]


# test_map_ids = [31, 79, 397, 17795]
test_map_ids = get_map_ids()
for id in test_map_ids:
    import ipdb; ipdb.set_trace()
    fix_map(id)
