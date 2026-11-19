import bpy, math, sys, os
from mathutils import Vector
D=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
def mat(name,col,metal=0.0,rough=0.4,emit=None,strength=0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    b=m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value=(*col,1); b.inputs["Metallic"].default_value=metal; b.inputs["Roughness"].default_value=rough
    if emit: b.inputs["Emission Color"].default_value=(*emit,1); b.inputs["Emission Strength"].default_value=strength
    return m
M={
 "coque":mat("coque",(0.014,0.015,0.018),0.15,0.42),
 "visiere":mat("visiere",(0.004,0.005,0.007),0.2,0.06),
 "liseres":mat("liseres",(0.95,0.33,0.03),0.1,0.35,(1.0,0.35,0.02),2.5),
 "lumieres":mat("lumieres",(1,0.4,0.05),0,0.3,(1.0,0.38,0.03),8),
 "oreilles":mat("oreilles",(0.05,0.05,0.055),0.85,0.3),
 "anneaux":mat("anneaux",(0.1,0.8,1),0,0.3,(0.1,0.75,1.0),10),
 "socle":mat("socle",(0.01,0.01,0.011),0.2,0.5),
}
for p in M:
    bpy.ops.wm.stl_import(filepath=os.path.join(D,p+".stl"))
    o=bpy.context.selected_objects[0]; o.name=p; o.scale=(0.001,)*3
    o.data.materials.append(M[p])
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.shade_smooth_by_angle(angle=math.radians(18))
# yeux : écrans posés sur la visière (lancer de rayon)
img=bpy.data.images.load(os.path.join(D,"oeil.png"))
me=bpy.data.materials.new("ecran"); me.use_nodes=True; nt=me.node_tree
bs=nt.nodes["Principled BSDF"]; tx=nt.nodes.new("ShaderNodeTexImage"); tx.image=img
nt.links.new(tx.outputs["Color"],bs.inputs["Base Color"]); nt.links.new(tx.outputs["Color"],bs.inputs["Emission Color"])
bs.inputs["Emission Strength"].default_value=2.2; bs.inputs["Roughness"].default_value=0.05
mb=mat("bord",(0.0,0.0,0.0),0.5,0.2)
dg=bpy.context.evaluated_depsgraph_get()
for x in (-0.036,0.036):
    hit,loc,nrm,i,ob,mx=sc.ray_cast(dg,Vector((x,-0.5,0.016)),Vector((0,1,0)))
    q=nrm.to_track_quat('Z','Y')
    bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=0.0255,depth=0.004,location=loc+nrm*0.0015)
    r=bpy.context.object; r.rotation_mode='QUATERNION'; r.rotation_quaternion=q; r.data.materials.append(mb)
    bpy.ops.mesh.primitive_circle_add(vertices=128,radius=0.0229,fill_type='NGON',location=loc+nrm*0.0037)
    e=bpy.context.object; e.rotation_mode='QUATERNION'; e.rotation_quaternion=q
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.uv.cylinder_project(); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.uv.project_from_view(camera_bounds=False) if False else None; bpy.ops.object.mode_set(mode='OBJECT')
    # UV planaires propres
    uv=e.data.uv_layers.active.data
    for poly in e.data.polygons:
        for li in poly.loop_indices:
            v=e.data.vertices[e.data.loops[li].vertex_index].co
            uv[li].uv=(v.x/0.0458+0.5, v.y/0.0458+0.5)
    e.data.materials.append(me)
# sol + fond
bpy.ops.mesh.primitive_plane_add(size=6,location=(0,0,-0.29)); fl=bpy.context.object
fl.data.materials.append(mat("sol",(0.006,0.006,0.008),0.2,0.32))
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.004,0.005,0.008,1)
def light(name,loc,energy,col,size):
    l=bpy.data.lights.new(name,'AREA'); l.energy=energy; l.color=col; l.size=size
    o=bpy.data.objects.new(name,l); sc.collection.objects.link(o); o.location=loc
    d=Vector((0,0,0.02))-Vector(loc); o.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
light("key",(0.9,-1.1,0.9),120,(1,0.97,0.92),0.9)
light("rimC",(-0.9,0.7,0.5),300,(0.3,0.75,1),0.6)
light("rimO",(0.8,0.8,0.3),220,(1,0.5,0.15),0.6)
light("top",(0,0.1,1.3),45,(1,1,1),1.2)
cam=bpy.data.cameras.new("cam"); cam.lens=70; co=bpy.data.objects.new("cam",cam); sc.collection.objects.link(co); sc.camera=co
sc.render.engine='CYCLES'; sc.cycles.samples=int(os.environ.get("SAMPLES","96")); sc.cycles.use_denoising=True
sc.render.resolution_x=1400; sc.render.resolution_y=1400
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
for nom,pos in [("face",(0.0,-1.55,0.12)),("trois_quarts",(0.95,-1.2,0.25)),("profil",(1.55,-0.2,0.08))]:
    co.location=pos; t=Vector((0,0.0,-0.02)); co.rotation_euler=(t-Vector(pos)).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=os.path.join(D,nom+".png"); bpy.ops.render.render(write_still=True)
