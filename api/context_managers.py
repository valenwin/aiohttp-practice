from contextlib import asynccontextmanager

from api.models import Session, session_context


@asynccontextmanager
async def session_manager(db_session=Session, expire_on_commit=False):
    """
    Context manager with parameter for async session usage.

    Example:

    async with get_session(Session) as session:
        reasons = await session.execute(query)
    """
    async with db_session(expire_on_commit=expire_on_commit) as session:
        async with session.begin():
            token = session_context.set(session)
            try:
                yield session
            finally:
                session_context.reset(token)
