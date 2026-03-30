"""Phase 1 tests: health endpoint, database connection, table creation, model defaults, enums."""

from sqlalchemy import inspect

from app.models import EventSource, EventType, Student, StudentStatus


class TestHealthEndpoint:
    """Verify the /health endpoint works correctly."""

    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_response_body(self, client):
        data = client.get("/health").json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"


class TestDatabaseConnection:
    """Verify database connectivity and setup."""

    def test_session_creates_and_closes(self, db_session):
        """DB session can be created and closed without error."""
        assert db_session is not None
        assert db_session.is_active

    def test_can_execute_query(self, db_session):
        from sqlalchemy import text

        result = db_session.execute(text("SELECT 1")).scalar()
        assert result == 1


class TestTablesCreated:
    """Verify all 4 tables exist after startup."""

    EXPECTED_TABLES = {"students", "parents", "cars", "pickup_events"}

    def test_all_tables_exist(self, db_session):
        inspector = inspect(db_session.bind)
        existing = set(inspector.get_table_names())
        assert self.EXPECTED_TABLES.issubset(existing), (
            f"Missing tables: {self.EXPECTED_TABLES - existing}"
        )

    def test_cars_plate_number_index_exists(self, db_session):
        inspector = inspect(db_session.bind)
        indexes = inspector.get_indexes("cars")
        index_names = {idx["name"] for idx in indexes}
        assert "ix_cars_plate_number" in index_names


class TestStudentModelDefaults:
    """Verify Student model creates with correct defaults."""

    def test_default_status_is_waiting(self, db_session):
        student = Student(name="Emma", grade="3A")
        db_session.add(student)
        db_session.commit()
        db_session.refresh(student)
        assert student.status == StudentStatus.WAITING

    def test_auto_generated_uuid(self, db_session):
        student = Student(name="Liam", grade="1B")
        db_session.add(student)
        db_session.commit()
        db_session.refresh(student)
        assert student.id is not None
        assert len(student.id) == 36  # UUID format

    def test_timestamps_set_on_create(self, db_session):
        student = Student(name="Sophia", grade="2C")
        db_session.add(student)
        db_session.commit()
        db_session.refresh(student)
        assert student.created_at is not None
        assert student.updated_at is not None


class TestEnumValues:
    """Verify enum values match the spec."""

    def test_student_status_values(self):
        values = {s.value for s in StudentStatus}
        assert values == {"WAITING", "ARRIVED", "SENT_TO_GATE", "PICKED_UP"}

    def test_event_type_values(self):
        values = {e.value for e in EventType}
        assert values == {"ARRIVED", "SENT", "PICKED"}

    def test_event_source_values(self):
        values = {e.value for e in EventSource}
        assert values == {"CAMERA", "APP", "MANUAL"}
