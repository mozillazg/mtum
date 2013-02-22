function toggleUserMenu(menu_id) {
  user_menu = document.getElementById(menu_id);
  if (!user_menu) return false;
  if (user_menu.style.display == 'none') {
    user_menu.style.display = 'block';
  } else {
    user_menu.style.display = 'none';
  }
}
