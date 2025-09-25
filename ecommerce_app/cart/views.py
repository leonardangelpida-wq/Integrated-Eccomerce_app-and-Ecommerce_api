import requests
from django.shortcuts import render
from django.http import JsonResponse

API_URL = "http://127.0.0.1:8001"  # FastAPI URL (make sure port matches uvicorn)

# ---------------- Cart Summary ----------------
def cart_summary(request):
    response = requests.get(f"{API_URL}/sales")
    orders = response.json() if response.status_code == 200 else []

    enriched_orders = []
    for order in orders:
        item_resp = requests.get(f"{API_URL}/items/{order['item_id']}")
        if item_resp.status_code == 200:
            item = item_resp.json()
            enriched_orders.append({
                "order_id": order["id"],
                "quantity": order["quantity"],
                "status": order["status"],
                "product": item  # product has image, price, name
            })

    return render(request, "cart_summary.html", {"orders": enriched_orders})


# ---------------- Add to Cart ----------------
def cart_add(request):
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        response = requests.post(
            f"{API_URL}/orders",
            json={
            "item_id": product_id,
            "quantity": product_qty,
            "status": "pending"
    }
)

        if response.status_code in [200, 201]:
            order_data = response.json()
            return JsonResponse({'qty': order_data["quantity"], "order_id": order_data["id"]})
        else:
            return JsonResponse({'error': response.text}, status=response.status_code)


# ---------------- Update Cart ----------------
def cart_update(request):
    if request.POST.get('action') == 'post':
        order_id = int(request.POST.get('order_id'))
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        payload = {
            "item_id": product_id,
            "quantity": product_qty,
            "status": "pending"
        }

        response = requests.put(f"{API_URL}/orders/{order_id}", json=payload)  # ✅ FIXED

        if response.status_code in [200, 201]:
            return JsonResponse({"success": True, "order": response.json()})
        else:
            return JsonResponse({"success": False, "error": response.text})


# ---------------- Delete Cart Item ----------------
def cart_delete(request):
    if request.POST.get('action') == 'post':
        order_id = int(request.POST.get('order_id'))

        response = requests.delete(f"{API_URL}/orders/{order_id}")  # ✅ FIXED
        if response.status_code in [200, 204]:
            return JsonResponse({"success": True, "message": f"Order {order_id} deleted"})
        else:
            return JsonResponse({"success": False, "error": response.text})
