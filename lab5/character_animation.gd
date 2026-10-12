
extends AnimationTree

const WALK_SPEED = 5.0
const RUN_SPEED = 10.0

func _ready() -> void:
	active = true
	update_animation(false, false, false, 0.0)

func update_animation(
	walking: bool,
	jumping: bool,
	attacking: bool,
	speed: float
) -> void:
	set("parameters/conditions/is_attacking", attacking)
	set("parameters/conditions/is_walking",
		walking and not jumping and not attacking)
	set("parameters/conditions/is_idle",
		not walking and not jumping and not attacking)
	set("parameters/conditions/is_jumping",
		jumping and not attacking)
	set("parameters/conditions/is_grounded", not jumping)

	set(
		"parameters/BlendSpace1D 2/blend_position",
		clampf(speed, WALK_SPEED, RUN_SPEED)
	)
