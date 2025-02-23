from shiny import reactive
from shiny.express import input, render, ui
import random

# import ret_no_gui
random.seed(10)

period = reactive.value(0)
demand = reactive.value(0)
inventory = reactive.value(25)
leadtime = reactive.value(2)
shipment_ret_queue = reactive.value([])

ui.page_opts(title="Retailer shipments")

with ui.sidebar():
    ui.input_numeric("shipment_size", "Distributor Shipment", value=10)
    ui.input_action_button("period_button", "Next period")


    @render.code
    def txt_p():
        return f'Period: {period()}'


    @render.code
    def txt_leadtime():
        return f'Leadtime: {leadtime()}'

ui.markdown(
    f"""
    Inventory management example
    """
)


# @render.ui
# def number():
#     return demand.get()

@render.code
def txt1():
    return f'Demand: {demand()}'


@render.code
def txt2():
    return f'Inventory: {inventory()}'


@reactive.effect
@reactive.event(input.period_button)
def period_actions():
    period.set(period() + 1)
    demand.set(random.randint(8, 12))
    inventory.set(max(inventory.get() - demand.get(), 0))
    shipment_ret_queue.set(shipment_ret_queue() + [(input.shipment_size(), period())])

    for row, (shipment, period_x) in enumerate(shipment_ret_queue()):
        if int(period_x) == period() - leadtime():
            cz = shipment
            shipment_ret_queue().pop(0)
            break
        else:
            cz = 0
    inventory.set(inventory.get() + cz)


@render.code
def out():
    return f"Shipments in transit: {shipment_ret_queue()}"


@render.image
def image():
    from pathlib import Path

    dir = Path(__file__).resolve().parent
    img: ImgData = {"src": str(dir / "distr_ret.png"), "width": "400px"}
    return img
