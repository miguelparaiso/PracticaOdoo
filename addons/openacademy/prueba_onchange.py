

# EJemplo de un onchange

def onchange_price(self, cr, uid, ids, unit_price, amount, context=None):
    """ Cambia el precio cada vez que cambia el precio unitario o la cantidad total"""
    return { 'value' : {'price' : unit_price * amount}}

