{% extends 'app/base.html' %}
{% load static %}
{% block content %}

      <div class="row">
        <div class="col-lg-4">
          <div class="row">
            <div class="col-xl-12">
              <div class="row">
                <div class="col-md-6">
                  <div class="card">
                    <div class="card-header mx-4 p-3 text-center">
                      <div class="icon icon-shape icon-lg bg-gradient-primary shadow text-center border-radius-lg">
                        <i class="fas fa-credit-card opacity-10"></i>
                      </div>
                    </div>
                    <div class="card-body pt-0 p-3 text-center">
                      <h6 class="text-center mb-0">Wallet</h6>
                      <span class="text-xs">Wallet Balance</span>
                      <hr class="horizontal dark my-3">
                      <h5 class="mb-0">₦{{ wallet_balance }}</h5>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="card">
                    <div class="card-header mx-4 p-3 text-center">
                      <div class="icon icon-shape icon-lg bg-gradient-primary shadow text-center border-radius-lg">
                        <i class="ni ni-money-coins opacity-10"></i>
                      </div>
                    </div>
                    <div class="card-body pt-0 p-3 text-center">
                      <form method="POST" action="{% url 'business-fund-wallet' %}">
                         {% csrf_token %}
                        <span class="text-xs">Enter amount to fund wallet</span>
                        <input type="number" class="form-control" placeholder="2000" name="amount" required>
                        <hr class="horizontal dark my-3">
                        <button type="submit" class="btn bg-gradient-dark mb-0"><i class="fas fa-plus"></i>&nbsp;&nbsp;Fund card</button>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-8">
          <div class="card h-100">
            <div class="col-md-12 mb-lg-0 mb-4">
              <div class="card mt-4">
                <div class="card-header pb-0 p-3">
                  <div class="row">
                    <div class="col-6 d-flex align-items-center">
                      <h6 class="mb-0">Payment Method</h6>
                    </div>
                  </div>
                </div>
                <div class="card-body p-3">
                  <div class="row">
                    {% for card in cards %}
                    <div class="col-md-6">
                      <div class="card card-body border card-plain border-radius-lg d-flex align-items-center flex-row">
                        {% if card.brand == "visa" %}
                        <img class="w-10 me-3 mb-0" src="{% static 'assets/img/logos/visa.png' %}" alt="{{ card.brand }}">
                        {% elif card.brand == "mastercard" %}
                        <img class="w-10 me-3 mb-0" src="{% static 'assets/img/logos/mastercard.png' %}" alt="{{ card.brand }}">
                        {% else %}
                        <img class="w-10 me-3 mb-0" src="{% static 'assets/img/logos/mastercard.png' %}" alt="{{ card.brand }}">
                        {% endif %}
                        <h6 class="mb-0">****&nbsp;&nbsp;&nbsp;****&nbsp;&nbsp;&nbsp;****&nbsp;&nbsp;&nbsp;{{ card.last_4 }}</h6>
                        <a class="btn btn-link text-danger text-gradient px-3 mb-0" href="{% url 'business-delete-card' card.id %}">
                          <i class="far fa-trash-alt me-2"></i>Delete
                        </a>

                      </div>
                    </div>
                    {% endfor %}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-7 mt-4">
          <div class="card h-100 mb-4">
            <div class="card-header pb-0 px-3">
              <div class="row">
                <div class="col-md-6">
                  <h6 class="mb-0">Your Transactions</h6>
                </div>
                <div class="card-header pb-0 p-3">
            </div>
              </div>
            </div>
            <div class="card-body pt-4 p-3">
              <h6 class="text-uppercase text-body text-xs font-weight-bolder mb-3">Newest</h6>
              <ul class="list-group">

                {% for transaction in transactions %}
                <li class="list-group-item border-0 d-flex justify-content-between ps-0 mb-2 border-radius-lg">
                  <div class="d-flex align-items-center">
                     {% if transaction.transaction_status == "SUCCESS" %}
                    <button class="btn btn-icon-only btn-rounded btn-outline-success mb-0 me-3 btn-sm d-flex align-items-center justify-content-center">
                      {% if transaction.transaction_type == "CREDIT" %}
                      <i class="fas fa-arrow-up"></i>
                      {% else %}
                      <i class="fas fa-arrow-down"></i>
                      {% endif %}
                    </button>
                      {% elif transaction.transaction_status == "FAILED" %}
                    <button class="btn btn-icon-only btn-rounded btn-outline-danger mb-0 me-3 btn-sm d-flex align-items-center justify-content-center">
                      {% if transaction.transaction_type == "CREDIT" %}
                      <i class="fas fa-arrow-up"></i>
                      {% else %}
                      <i class="fas fa-arrow-down"></i>
                      {% endif %}
                    </button>
                    {% elif transaction.transaction_status == "PENDING" %}
                    <button class="btn btn-icon-only btn-rounded btn-outline-dark mb-0 me-3 btn-sm d-flex align-items-center justify-content-center">
                      {% if transaction.transaction_type == "CREDIT" %}
                      <i class="fas fa-arrow-up"></i>
                      {% else %}
                      <i class="fas fa-arrow-down"></i>
                      {% endif %}
                    </button>
                     {% endif %}
                    <div class="d-flex flex-column">
                      <h6 class="mb-1 text-dark text-sm">{{ transaction.reference }}</h6>
                      <span class="text-xs">{{ transaction.created_at }}</span>
                    </div>
                  </div>

                  {% if transaction.transaction_status == "SUCCESS" %}
                    <div class="d-flex align-items-center text-success text-gradient text-sm font-weight-bold">
                        {{ transaction.transaction_status }}
                      <button class="btn btn-link text-dark text-sm mb-0 px-0 ms-4">{% if transaction.transaction_type == "CREDIT" %} + {% else %} - {% endif %}
                        ₦{{ transaction.amount }}</button>
                    </div>
                  {% elif transaction.transaction_status == "PENDING" %}
                    <div class="d-flex align-items-center text-dark text-gradient text-sm font-weight-bold">
                        {{ transaction.transaction_status }}
                      <button class="btn btn-link text-dark text-sm mb-0 px-0 ms-4"> {% if transaction.transaction_type == "CREDIT" %} + {% else %} - {% endif %}
                        ₦{{ transaction.amount }}</button>
                    </div>
                  {% elif transaction.transaction_status == "FAILED" %}
                    <div class="d-flex align-items-center text-danger text-gradient text-sm font-weight-bold">
                        {{ transaction.transaction_status }}
                      <button class="btn btn-link text-dark text-sm mb-0 px-0 ms-4"> {% if transaction.transaction_type == "CREDIT" %} + {% else %} - {% endif %}
                        ₦{{ transaction.amount }}</button>
                    </div>
                  {% endif %}
                </li>
                {% endfor %}

              </ul>
                  <ul class="pagination justify-content-center mt-4">
                    {% if transactions.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page=1">Ft</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ transactions.previous_page_number }}">Pr</a>
                    </li>
                    {% endif %}
                    {% for num in transactions.paginator.page_range %}
                    <li class="page-item {% if num == transactions.number %}active{% endif %}">
                        <a class="page-link" href="?page={{ num }}">{{ num }}</a>
                    </li>
                    {% endfor %}
                    {% if transactions.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ transactions.next_page_number }}">Nx</a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="?page={{ transactions.paginator.num_pages }}">Lt</a>
                    </li>
                    {% endif %}
                </ul>
            </div>
          </div>
        </div>
<!--        <div class="col-md-5 mt-4">-->
<!--          <div class="card">-->
<!--            <div class="card-header pb-0 px-3">-->
<!--              <h6 class="mb-0">Bank Accounts</h6>-->
<!--            </div>-->
<!--            <div class="card-body pt-4 p-3">-->
<!--              <ul class="list-group">-->
<!--                {% for bank_account in bank_accounts %}-->
<!--                <li class="list-group-item border-0 d-flex p-4 mb-2 bg-gray-100 border-radius-lg">-->
<!--                  <div class="d-flex flex-column">-->
<!--                    <h6 class="mb-3 text-sm">{{ bank_account.account_name }}</h6>-->
<!--                    <span class="mb-2 text-xs">Bank Name: <span class="text-dark font-weight-bold ms-sm-2">{{ bank_account.bank_name }}</span></span>-->
<!--                    <span class="text-xs">Account Number: <span class="text-dark ms-sm-2 font-weight-bold">{{ bank_account.account_number }}</span></span>-->
<!--                  </div>-->
<!--                  <div class="ms-auto text-end">-->
<!--                    <a class="btn btn-link text-danger text-gradient px-3 mb-0" href="javascript:;"><i class="far fa-trash-alt me-2"></i>Delete</a>-->
<!--                    <a class="btn btn-link text-dark px-3 mb-0" href="javascript:;"><i class="fas fa-pencil-alt text-dark me-2" aria-hidden="true"></i>Edit</a>-->
<!--                  </div>-->
<!--                </li>-->
<!--                {% endfor %}-->
<!--              </ul>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
      </div>


{% endblock %}
