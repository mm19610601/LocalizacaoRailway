from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Utilizador, Localizacao
from datetime import datetime, timedelta
from sqlalchemy import and_, or_
import logging

@app.route('/')
def index():
    """Main dashboard with map and recent locations"""
    try:
        # Get recent locations (last 24 hours)
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_locations = db.session.query(Localizacao).filter(
            Localizacao.timestamp >= yesterday
        ).order_by(Localizacao.timestamp.desc()).limit(100).all()
        
        # Get all users for filter dropdown
        users = db.session.query(Utilizador).order_by(Utilizador.nome_completo).all()
        
        # Convert locations to dict for JavaScript
        locations_data = [loc.to_dict() for loc in recent_locations]
        
        return render_template('index.html', 
                             locations=locations_data, 
                             users=users,
                             total_locations=len(locations_data))
    except Exception as e:
        logging.error(f"Error in index route: {e}")
        flash(f"Erro ao carregar dados: {str(e)}", "error")
        return render_template('index.html', locations=[], users=[], total_locations=0)

@app.route('/users')
def users():
    """User management page"""
    try:
        users = db.session.query(Utilizador).order_by(Utilizador.nome_completo).all()
        return render_template('users.html', users=users)
    except Exception as e:
        logging.error(f"Error in users route: {e}")
        flash(f"Erro ao carregar utilizadores: {str(e)}", "error")
        return render_template('users.html', users=[])

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    """Add new user"""
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            nome_completo = request.form.get('nome_completo')
            funcao = request.form.get('funcao')
            telemovel = request.form.get('telemovel')
            
            # Check if username already exists
            existing_user = db.session.query(Utilizador).filter_by(username=username).first()
            if existing_user:
                flash("Nome de utilizador já existe!", "error")
                return redirect(url_for('users'))
            
            # Create new user
            new_user = Utilizador()
            new_user.username = username
            new_user.password = password  # In production, hash this password
            new_user.nome_completo = nome_completo
            new_user.funcao = funcao
            new_user.telemovel = telemovel
            
            db.session.add(new_user)
            db.session.commit()
            
            flash("Utilizador adicionado com sucesso!", "success")
            return redirect(url_for('users'))
            
        except Exception as e:
            logging.error(f"Error adding user: {e}")
            db.session.rollback()
            flash(f"Erro ao adicionar utilizador: {str(e)}", "error")
            return redirect(url_for('users'))
    
    return redirect(url_for('users'))

@app.route('/user/delete/<int:user_id>')
def delete_user(user_id):
    """Delete user"""
    try:
        user = db.session.get(Utilizador, user_id)
        if not user:
            flash("Utilizador não encontrado", "error")
            return redirect(url_for('users'))
        db.session.delete(user)
        db.session.commit()
        flash("Utilizador removido com sucesso!", "success")
    except Exception as e:
        logging.error(f"Error deleting user: {e}")
        db.session.rollback()
        flash(f"Erro ao remover utilizador: {str(e)}", "error")
    
    return redirect(url_for('users'))

@app.route('/locations')
def locations():
    """Detailed locations view with filtering"""
    try:
        # Get filter parameters
        user_id = request.args.get('user_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        page = request.args.get('page', 1, type=int)
        per_page = 50
        
        # Build query
        query = db.session.query(Localizacao)
        
        # Filter by user
        if user_id:
            query = query.filter(Localizacao.user_id == user_id)
        
        # Filter by date range
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(Localizacao.timestamp >= start_dt)
            except ValueError:
                flash("Data de início inválida", "error")
        
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Localizacao.timestamp < end_dt)
            except ValueError:
                flash("Data de fim inválida", "error")
        
        # Order by timestamp descending
        query = query.order_by(Localizacao.timestamp.desc())
        
        # Get results with limit
        locations = query.limit(per_page).offset((page - 1) * per_page).all()
        
        # Simple pagination info
        total_count = query.count()
        has_prev = page > 1
        has_next = len(locations) == per_page
        pagination = type('Pagination', (), {
            'items': locations,
            'has_prev': has_prev,
            'has_next': has_next,
            'page': page,
            'prev_num': page - 1 if has_prev else None,
            'next_num': page + 1 if has_next else None
        })()
        
        # Get all users for filter dropdown
        users = db.session.query(Utilizador).order_by(Utilizador.nome_completo).all()
        
        return render_template('locations.html', 
                             locations=locations,
                             users=users,
                             pagination=pagination,
                             current_filters={
                                 'user_id': user_id,
                                 'start_date': start_date,
                                 'end_date': end_date
                             })
        
    except Exception as e:
        logging.error(f"Error in locations route: {e}")
        flash(f"Erro ao carregar localizações: {str(e)}", "error")
        return render_template('locations.html', locations=[], users=[], pagination=None)

@app.route('/get_users')
def get_users():
    """API endpoint to get users data"""
    try:
        users = db.session.query(Utilizador).order_by(Utilizador.nome_completo).all()
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'nome_completo': user.nome_completo,
                'funcao': user.funcao,
                'telemovel': user.telemovel
            })
        return jsonify(users_data)
    except Exception as e:
        logging.error(f"Error getting users: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/locations')
def api_locations():
    """API endpoint for getting locations (for map updates)"""
    try:
        user_id = request.args.get('user_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = request.args.get('limit', 1000, type=int)
        
        # Build query
        query = db.session.query(Localizacao)
        
        if user_id:
            query = query.filter(Localizacao.user_id == user_id)
        
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(Localizacao.timestamp >= start_dt)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Localizacao.timestamp < end_dt)
            except ValueError:
                pass
        
        locations = query.order_by(Localizacao.timestamp.desc()).limit(limit).all()
        
        return jsonify([loc.to_dict() for loc in locations])
        
    except Exception as e:
        logging.error(f"Error in API locations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/location/add', methods=['POST'])
def add_location():
    """Add new location data"""
    try:
        user_id = request.form.get('user_id', type=int)
        latitude = request.form.get('latitude', type=float)
        longitude = request.form.get('longitude', type=float)
        precisao = request.form.get('precisao', type=float)
        
        if not user_id or latitude is None or longitude is None:
            flash("Dados de localização incompletos", "error")
            return redirect(url_for('index'))
        
        # Verify user exists
        user = db.session.query(Utilizador).get(user_id)
        if not user:
            flash("Utilizador não encontrado", "error")
            return redirect(url_for('index'))
        
        # Create new location
        new_location = Localizacao()
        new_location.user_id = user_id
        new_location.latitude = latitude
        new_location.longitude = longitude  
        new_location.precisao = precisao
        new_location.timestamp = datetime.utcnow()
        
        db.session.add(new_location)
        db.session.commit()
        
        flash("Localização adicionada com sucesso!", "success")
        
    except Exception as e:
        logging.error(f"Error adding location: {e}")
        db.session.rollback()
        flash(f"Erro ao adicionar localização: {str(e)}", "error")
    
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('base.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html'), 500
