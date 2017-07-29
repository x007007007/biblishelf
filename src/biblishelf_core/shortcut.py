

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
        return m, True

def create_or_update(s, model, default=None, **kwargs):
    ms = s.query(model).filter_by(
        **kwargs
    )
    if ms.count()>0:
        ms.update(
            default,
            synchronize_session='evaluate'
        )
        s.commit()
        return ms.first(), True
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
        return m, False