

def get_or_create(s, model, default=None, **kwargs):
    is_create = False
    m = s.query(model).filter_by(
        **kwargs
    ).first()
    if m:
        return m, False
    else:
        c_kwargs = {}
        c_kwargs.update(**kwargs)
        if default is not None:
            c_kwargs.update(default)
        m = model(
            **c_kwargs
        )
        s.add(m)
        s.commit()
        return m, True

def create_or_update(s, model, default=None, **kwargs):
    m = s.query(model).filter_by(
        **kwargs
    ).first()
    if m:
        s.query(model).filter_by(
            **kwargs,
        ).update(
            **default
        )
        return s.query(model).filter_by(
            **kwargs
        ).first(), True
    else:
        c_kwargs = {}
        c_kwargs.update(**kwargs)
        if default is not None:
            c_kwargs.update(default)
        default.update(**kwargs)
        m = model(
            **c_kwargs
        )
        s.add(m)
        s.commit()
        return m, False