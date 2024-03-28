{% extends 'app/base.html' %}

{% block content %}

    <div class="row">
        <div class="col-12 col-xl-12">
          <div class="card h-100">
            <div class="card-header pb-0 p-3">
              <h6 class="mb-0">Platform Settings</h6>
            </div>
            <div class="card-body p-3">
              <h6 class="text-uppercase text-body text-xs font-weight-bolder">Account</h6>
              <ul class="list-group">
                <li class="list-group-item border-0 px-0">
                  <div class="form-check form-switch ps-0">
                    <input class="form-check-input ms-auto" type="checkbox" id="flexSwitchCheckDefault" checked>
                    <label class="form-check-label text-body ms-3 text-truncate w-80 mb-0" for="flexSwitchCheckDefault">Email me when someone follows me</label>
                  </div>
                </li>
                <li class="list-group-item border-0 px-0">
                  <div class="form-check form-switch ps-0">
                    <input class="form-check-input ms-auto" type="checkbox" id="flexSwitchCheckDefault1">
                    <label class="form-check-label text-body ms-3 text-truncate w-80 mb-0" for="flexSwitchCheckDefault1">Email me when someone answers on my post</label>
                  </div>
                </li>
                <li class="list-group-item border-0 px-0">
                  <div class="form-check form-switch ps-0">
                    <input class="form-check-input ms-auto" type="checkbox" id="flexSwitchCheckDefault2" checked>
                    <label class="form-check-label text-body ms-3 text-truncate w-80 mb-0" for="flexSwitchCheckDefault2">Email me when someone mentions me</label>
                  </div>
                </li>
              </ul>
              <h6 class="text-uppercase text-body text-xs font-weight-bolder mt-4">Application</h6>
              <ul class="list-group">
                <li class="list-group-item border-0 px-0">
                  <div class="form-check form-switch ps-0">
                    <input class="form-check-input ms-auto" type="checkbox" id="flexSwitchCheckDefault3">
                    <label class="form-check-label text-body ms-3 text-truncate w-80 mb-0" for="flexSwitchCheckDefault3">New launches and projects</label>
                  </div>
                </li>
                <li class="list-group-item border-0 px-0">
                  <div class="form-check form-switch ps-0">
                    <input class="form-check-input ms-auto" type="checkbox" id="flexSwitchCheckDefault4" checked>
                    <label class="form-check-label text-body ms-3 text-truncate w-80 mb-0" for="flexSwitchCheckDefault4">Monthly product updates</label>
                  </div>
                </li>
                <li class="list-group-item border-0 px-0 pb-0">
                  <div class="form-check form-switch ps-0">
                    <input class="form-check-input ms-auto" type="checkbox" id="flexSwitchCheckDefault5">
                    <label class="form-check-label text-body ms-3 text-truncate w-80 mb-0" for="flexSwitchCheckDefault5">Subscribe to newsletter</label>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>


         <div class="col-12 mt-4">
          <div class="card h-100">
            <div class="card-header pb-0 p-3">
              <h6 class="mb-0">API Key & webhooks</h6>
            </div>
            <div class="card-body p-3">
              <div class="mb-3">
                <label class="form-check-label" for="secretKey">
                  Secret key
                </label>
                  <input id="secretKey" type="password" class="form-control" value="{{ secret_key }}" readonly>
                    <span id="toggleVisibility" class="fa fa-eye" style="cursor: pointer;"></span>
                <p class="text-sm mt-3 mb-0"><a href="{% url 'business-regenerate-secret-key' %}" class="text-dark font-weight-bolder">Generate a new secret key</a></p>

              </div>

                <form method="post" role="form text-left">
                  {% csrf_token %}
                  <div class="mb-3">
                   <label class="form-check-label" for="webhookUrl">
                      Webhook url
                    </label>
                     <input id="webhookUrl" type="text" class="form-control" placeholder="https://example.com/webhook-url"  name="webhook_url" {% if current_webhook_url %} value="{{ current_webhook_url }}"{% endif %}>
                    {% for error in form.webhook_url.errors %}
                      <span class="text-danger error-message">{{ error }}</span>
                  {% endfor %}
                  </div>
                  <div class="text-center">
                    <button type="submit" class="btn bg-gradient-dark w-100 my-4 mb-2">Change webhook url</button>
                  </div>
                </form>
              </div>
          </div>
        </div>
      </div>

<script>
    // JavaScript
    document.getElementById("toggleVisibility").addEventListener("click", function() {
        var secretKeyInput = document.getElementById("secretKey");
        if (secretKeyInput.type === "password") {
            secretKeyInput.type = "text";
        } else {
            secretKeyInput.type = "password";
        }
    });
</script>


{% endblock %}
