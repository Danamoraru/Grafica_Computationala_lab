
extends CharacterBody3D

const SPEED = 5.0
const RUN_SPEED = 10.0
const JUMP_VELOCITY = 4.5
const ATTACK_DURATION = 1.083

@onready var animation_controller = $AnimationTree
@onready var character_model: Node3D = $Character_Gun

var is_attacking = false
var facing_angle = 0.0
var attack_timer = 0.0

func _ready() -> void:
	update_animations()

func _physics_process(delta: float) -> void:
	apply_gravity(delta)

	if is_attacking:
		process_attack(delta)
		return

	process_jump()
	process_movement()
	move_and_slide()
	update_animations()

func apply_gravity(delta: float) -> void:
	if not is_on_floor():
		velocity += get_gravity() * delta

func process_jump() -> void:
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = JUMP_VELOCITY

func process_movement() -> void:
	var direction_x = Input.get_axis("ui_left", "ui_right")
	var direction_y = Input.get_axis("ui_up", "ui_down")
	var speed = SPEED

	if Input.is_physical_key_pressed(KEY_SHIFT):
		speed = RUN_SPEED

	velocity.x = direction_x * speed
	velocity.z = direction_y * speed

	if direction_x > 0:
		facing_angle = PI / 2
	elif direction_x < 0:
		facing_angle = -PI / 2

	if Input.is_physical_key_pressed(KEY_W):
		facing_angle = 0.0

	character_model.rotation.y = facing_angle

func update_animations() -> void:
	var walking = abs(velocity.x) > 0.1 or abs(velocity.z) > 0.1
	var jumping = not is_on_floor()

	animation_controller.update_animation(
		walking,
		jumping,
		is_attacking,
		abs(velocity.x)
	)

func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey:
		if event.physical_keycode == KEY_F and event.pressed and not event.echo:
			if not is_attacking and is_on_floor():
				start_attack()

func start_attack() -> void:
	is_attacking = true
	attack_timer = ATTACK_DURATION
	update_animations()

func process_attack(delta: float) -> void:
	attack_timer -= delta
	velocity.x = 0.0
	velocity.z = 0.0
	move_and_slide()

	if attack_timer <= 0.0:
		finish_attack()

func on_punch_hit() -> void:
	print("Персонаж выполнил удар!")

func finish_attack() -> void:
	if not is_attacking:
		return

	is_attacking = false
	attack_timer = 0.0
	update_animations()
	print("Управление восстановлено")
